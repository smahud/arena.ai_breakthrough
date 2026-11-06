"""AgentLoop: plan → select-ready → dispatch (parallel where independent) → reflect →
recover/validate → checkpoint → terminate. Shape mirrors the observed lifecycle
(docs/execution-lifecycle.md); parallelism justified by F-01/F-09."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from .recovery import RecoveryPolicy
from .state import StateStore, TraceReporter
from .tools import default_registry
from .types import DONE, FAILED, PENDING, Task
from .validate import Validator


def decompose_from_dicts(specs):
    """Deterministic default decomposition provider.

    Provider interface (directive §5 'configurable model-provider interfaces'): any callable
    goal -> list[Task] can be supplied to AgentLoop.plan_with(); an LLM-backed provider would
    replace this function without touching the loop. Default stays deterministic for
    testability and C-1 compliance — no vendor SDK is wired speculatively.
    """
    return [Task(id=s["id"], tool=s.get("tool", "shell"), payload=s.get("payload", {}),
                 deps=tuple(s.get("deps", ())), validate=s.get("validate"),
                 repair=s.get("repair"), max_attempts=s.get("max_attempts", 2))
            for s in specs]


@dataclass
class RunSummary:
    all_ok: bool
    statuses: dict
    attempts_total: int
    trace_path: str
    failures: list = field(default_factory=list)


class AgentLoop:
    def __init__(self, trace_path, state_path=None, registry=None, validator=None,
                 max_workers=4, replan_fn=None, replan_budget=1):
        self.registry = registry or default_registry()
        self.trace = TraceReporter(trace_path)
        self.state = StateStore(state_path)
        self.validator = validator or Validator(self.registry)
        self.max_workers = max_workers   # 4 = 2x measured vCPU count (F-09)
        self.replan_fn = replan_fn
        self.replan_budget = replan_budget

    def plan_with(self, decompose_fn, goal):
        tasks = decompose_fn(goal)
        self.trace.event(type="plan", tasks=[t.id for t in tasks],
                         deps={t.id: list(t.deps) for t in tasks})
        return tasks

    def run(self, tasks):
        by_id = {t.id: t for t in tasks}
        replans_used = 0
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            while True:
                self._propagate_dep_failures(by_id)
                ready = [t for t in tasks if t.status == PENDING
                         and all(d in by_id and by_id[d].status == DONE for d in t.deps)]
                if not ready:
                    pending = [t for t in tasks if t.status == PENDING]
                    if pending and self.replan_fn and replans_used < self.replan_budget:
                        replans_used += 1
                        self.trace.event(type="replan", used=replans_used,
                                         pending=[t.id for t in pending])
                        self.replan_fn(tasks)
                        continue
                    for t in pending:
                        t.status = FAILED
                        self.trace.event(type="unreachable", task=t.id,
                                         reason="dependency cycle or missing dep")
                    break
                futures = {ex.submit(self._execute, t): t for t in ready}
                for fut in as_completed(futures):
                    fut.result()
                self.state.update(tasks)
                self.state.save()
                if all(t.status in (DONE, FAILED) for t in tasks):
                    break
        self.state.update(tasks)
        self.state.save()
        summary = RunSummary(
            all_ok=all(t.status == DONE for t in tasks),
            statuses={t.id: t.status for t in tasks},
            attempts_total=sum(t.attempts for t in tasks),
            trace_path=self.trace.path,
            failures=[t.id for t in tasks if t.status == FAILED],
        )
        self.trace.event(type="run_summary", all_ok=summary.all_ok,
                         statuses=summary.statuses, attempts=summary.attempts_total)
        return summary

    def _propagate_dep_failures(self, by_id):
        changed = True
        while changed:
            changed = False
            for t in by_id.values():
                if t.status == PENDING and any(
                        d in by_id and by_id[d].status == FAILED for d in t.deps):
                    t.status = FAILED
                    self.trace.event(type="dep_failed", task=t.id,
                                     failed_deps=[d for d in t.deps
                                                  if d in by_id and by_id[d].status == FAILED])
                    changed = True

    def _execute(self, task):
        tool = self.registry.get(task.tool)
        task.attempts += 1
        result = tool(task.payload)
        task.result = result
        self.trace.event(type="tool_result", task=task.id, attempt=task.attempts,
                         tool=task.tool, command=result.command, ok=result.ok,
                         exit_code=result.exit_code, duration_ms=result.duration_ms,
                         output_tail=result.output[-400:])
        if result.ok and task.validate:
            vok, detail = self.validator.check(task.validate)
            self.trace.event(type="validation", task=task.id, ok=vok, detail=detail)
            if not vok:
                result = type(result)(False, detail, result.exit_code,
                                      result.duration_ms, result.command)
                task.result = result
        if result.ok:
            task.status = DONE
            return
        cls = RecoveryPolicy.classify(result)
        self.trace.event(type="failure_classified", task=task.id, cls=cls,
                         attempt=task.attempts)
        if task.attempts < task.max_attempts:
            if RecoveryPolicy.attempt_repair(task, result):
                self.trace.event(type="repair_applied", task=task.id, attempt=task.attempts)
                task.status = PENDING   # retry on next wave (F-02: re-run after patch)
                return
            if task.blind_retries > 0 and task.attempts <= task.blind_retries:
                # EXP-09: transient fault — identical re-run may succeed; no patch applied.
                self.trace.event(type="blind_retry", task=task.id, attempt=task.attempts,
                                 remaining=min(task.blind_retries, task.max_attempts - 1) - task.attempts + 1)
                task.status = PENDING
                return
        task.status = FAILED    # reported, never concealed (contract rule 9)
