"""Recovery policy (JUSTIFICATIONS row 7; findings F-02, Exp-03 fault classes)."""


class RecoveryPolicy:
    """Classify a failure the way the observed recovery loop did: by exit code + error text."""

    @staticmethod
    def classify(result):
        out = result.output or ""
        if result.exit_code == 127:
            return "environment"      # Exp-03 F3a: command not found
        if "SyntaxError" in out:
            return "compile"          # Exp-03 F1
        if "FAILED" in out or "AssertionError" in out:
            return "test"             # Exp-03 F2
        if result.exit_code is None:
            return "timeout"          # Exp-05 P4 hang class
        return "runtime"              # Exp-03 F3b

    @staticmethod
    def attempt_repair(task, result):
        """F-02 loop step 'minimal patch': delegated to the task's repair fn if registered.
        No speculative auto-rollback engine (limitations L-5; contract rule 3)."""
        if task.repair is None:
            return False
        return bool(task.repair(task, task.attempts, result))
