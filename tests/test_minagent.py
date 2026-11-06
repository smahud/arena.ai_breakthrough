"""minagent tests: each maps to the finding that justifies the component under test."""
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from minagent import (AgentLoop, StateStore, Task, ToolResult, Validator,  # noqa: E402
                      default_registry, decompose_from_dicts)
from minagent.recovery import RecoveryPolicy  # noqa: E402
from minagent.tools import shell_tool  # noqa: E402


@pytest.fixture
def loop(tmp_path):
    return AgentLoop(trace_path=str(tmp_path / "trace.jsonl"),
                     state_path=str(tmp_path / "state.json"))


def read_trace(loop):
    return loop.trace.read()


def test_shell_adapter_pipefail_encodes_F03():
    r = shell_tool({"command": "false | true"})
    assert not r.ok and r.exit_code == 1  # without pipefail this would be a false green
    r2 = shell_tool({"command": "echo hi | tee /dev/null"})
    assert r2.ok and "hi" in r2.output


def test_write_adapter_atomic_roundtrip(tmp_path):
    reg = default_registry()
    p = str(tmp_path / "a.txt")
    res = reg.get("write_file")({"path": p, "content": "payload"})
    assert res.ok and open(p).read() == "payload"


def test_recovery_classification_matches_exp03():
    assert RecoveryPolicy.classify(ToolResult(False, "", 127)) == "environment"
    assert RecoveryPolicy.classify(ToolResult(False, "SyntaxError: expected ':'", 1)) == "compile"
    assert RecoveryPolicy.classify(ToolResult(False, "FAILED t::x - assert 2 == 3", 1)) == "test"
    assert RecoveryPolicy.classify(ToolResult(False, "timeout", None)) == "timeout"
    assert RecoveryPolicy.classify(ToolResult(False, "FileNotFoundError", 1)) == "runtime"


def test_dependency_ordering(loop, tmp_path):
    f = tmp_path / "dep.txt"
    tasks = decompose_from_dicts([
        {"id": "B", "deps": ["A"], "payload": {"command": f"cat {f}"}},
        {"id": "A", "payload": {"command": f"echo written > {f}"}},
    ])
    s = loop.run(tasks)
    assert s.all_ok and s.statuses == {"A": "done", "B": "done"}
    ev = [e for e in read_trace(loop) if e["type"] == "tool_result"]
    assert ev[0]["task"] == "A" and ev[1]["task"] == "B"  # dep strictly first


def test_independent_tasks_run_concurrently_F01(loop):
    tasks = decompose_from_dicts([
        {"id": f"s{i}", "payload": {"command": "sleep 0.25 && echo ok"}} for i in range(3)
    ])
    t0 = time.monotonic()
    s = loop.run(tasks)
    wall = time.monotonic() - t0
    assert s.all_ok
    assert wall < 0.6, f"3x0.25s sleeps took {wall:.2f}s — expected overlap"


def test_recovery_loop_F02(loop, tmp_path):
    missing = tmp_path / "missing.txt"

    def repair(task, attempt, result):
        assert attempt == 1
        missing.write_text("now here")   # minimal patch, 1 action
        return True

    tasks = [Task(id="r", payload={"command": f"cat {missing}"}, repair=repair)]
    s = loop.run(tasks)
    assert s.all_ok and s.attempts_total == 2
    types = [e["type"] for e in read_trace(loop)]
    assert "failure_classified" in types and "repair_applied" in types


def test_retry_budget_exhausted_reported_not_concealed(loop):
    """Semantics (recovery of an organic test failure, 14:13Z): retry happens only AFTER a
    successful repair (F-02 loop shape: detect→localize→patch→re-verify). A repair that
    returns False terminates the task immediately — blind re-runs of deterministic failures
    are not retried. Original expectation (2 events) was wrong; fixed in 1 line."""
    tasks = [Task(id="f", payload={"command": "exit 3"}, repair=lambda t, a, r: False,
                  max_attempts=2)]
    s = loop.run(tasks)
    assert not s.all_ok and s.failures == ["f"] and s.statuses["f"] == "failed"
    assert s.attempts_total == 1  # no blind retry without a patch
    assert sum(1 for e in read_trace(loop) if e["type"] == "failure_classified") == 1


def test_false_green_guard_F03_F08(loop):
    """Exit 0 + success-shaped output but zero work done must FAIL validation."""
    spec = {"command": "echo 'Ran 0 tests in 0.000s'; echo 'NO TESTS RAN'",
            "expect": ["Ran"], "forbid": ["NO TESTS RAN"]}
    tasks = [Task(id="fg", payload={"command": "true"}, validate=spec)]
    s = loop.run(tasks)
    assert s.statuses["fg"] == "failed"
    v = [e for e in read_trace(loop) if e["type"] == "validation"]
    assert "false-green marker present" in v[-1]["detail"]


def test_validator_accepts_positive_evidence():
    ok, detail = Validator().check({"command": "echo '10 passed in 0.02s'",
                                    "expect": ["passed"], "forbid": ["NO TESTS RAN"]})
    assert ok and detail == "validated"


def test_dep_failure_propagation(loop):
    tasks = decompose_from_dicts([
        {"id": "A", "payload": {"command": "exit 1"}},
        {"id": "B", "deps": ["A"], "payload": {"command": "echo never"}},
    ])
    s = loop.run(tasks)
    assert s.statuses == {"A": "failed", "B": "failed"}
    b = [t for t in tasks if t.id == "B"][0]
    assert b.attempts == 0  # isolated without execution (F-15 analogue)
    assert any(e["type"] == "dep_failed" for e in read_trace(loop))


def test_state_persistence_exp06_pattern(loop, tmp_path):
    tasks = decompose_from_dicts([{"id": "A", "payload": {"command": "true"}}])
    loop.run(tasks)
    reloaded = StateStore.load(loop.state.path)
    assert reloaded.data["tasks"]["A"]["status"] == "done"


def test_replan_hook_single_budget(loop):
    tasks = decompose_from_dicts([
        {"id": "A", "payload": {"command": "true"}},
        {"id": "B", "deps": ["GHOST"], "payload": {"command": "true"}},
    ])
    calls = []

    def replan(ts):
        calls.append(1)
        for t in ts:
            if t.id == "B":
                t.deps = ("A",)   # dynamic replan: drop unsatisfiable dep

    loop.replan_fn = replan
    s = loop.run(tasks)
    assert s.all_ok and len(calls) == 1  # budget consumed exactly once


FLAKY_CMD = ('n=$(cat {c} 2>/dev/null || echo 0); n=$((n+1)); echo $n > {c}; '
             'if [ "$n" -ge 2 ]; then echo "OK attempt $n"; else echo "flaky failure attempt $n"; exit 1; fi')


def test_blind_retry_recovers_transient_fault_exp09(loop, tmp_path):
    cmd = FLAKY_CMD.format(c=tmp_path / "c")
    tasks = [Task(id="flaky", payload={"command": cmd}, blind_retries=1, max_attempts=2)]
    s = loop.run(tasks)
    assert s.all_ok and s.attempts_total == 2          # succeeded on identical re-run
    assert any(e["type"] == "blind_retry" for e in read_trace(loop))
    assert "OK attempt 2" in tasks[0].result.output


def test_blind_retry_default_zero_preserves_f02(loop, tmp_path):
    """Same flaky command, default policy: no patch -> no retry (Exp-09 'before' behavior)."""
    cmd = FLAKY_CMD.format(c=tmp_path / "c2")
    tasks = [Task(id="flaky", payload={"command": cmd})]
    s = loop.run(tasks)
    assert s.statuses["flaky"] == "failed" and s.attempts_total == 1


def test_blind_retry_exhaustion_still_reports(loop, tmp_path):
    """Always-failing command with blind_retries: bounded, then FAILED (never concealed)."""
    tasks = [Task(id="doomed", payload={"command": "exit 7"}, blind_retries=3, max_attempts=3)]
    s = loop.run(tasks)
    assert s.statuses["doomed"] == "failed" and s.attempts_total == 3
    assert sum(1 for e in read_trace(loop) if e["type"] == "blind_retry") == 2


def test_e2e_mini_project(loop, tmp_path):
    """Exp-02-shaped project: 3 independent streams + aggregation with validation."""
    d = tmp_path
    tasks = decompose_from_dicts([
        {"id": "a", "tool": "write_file",
         "payload": {"path": str(d / "a.txt"), "content": "alpha"}},
        {"id": "b", "tool": "write_file",
         "payload": {"path": str(d / "b.txt"), "content": "beta"}},
        {"id": "c", "tool": "write_file",
         "payload": {"path": str(d / "c.txt"), "content": "gamma"}},
        {"id": "agg", "deps": ["a", "b", "c"],
         "payload": {"command": f"cat {d}/a.txt {d}/b.txt {d}/c.txt"},
         "validate": {"command": f"ls {d}/*.txt | wc -l",
                      "expect": ["3"], "forbid": ["No such file"]}},
    ])
    s = loop.run(tasks)
    assert s.all_ok and s.statuses["agg"] == "done"
    assert open(d / "a.txt").read() == "alpha"
