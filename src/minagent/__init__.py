"""minagent — minimal agentic reference implementation.

Stdlib only (C-1). Every component is justified in reference-architecture/JUSTIFICATIONS.md;
nothing speculative is included (contract rule 3).
"""
__version__ = "0.1.0"

from .types import Task, ToolResult, PENDING, RUNNING, DONE, FAILED  # noqa: F401
from .tools import ToolRegistry, default_registry  # noqa: F401
from .state import StateStore, TraceReporter  # noqa: F401
from .validate import Validator  # noqa: F401
from .recovery import RecoveryPolicy  # noqa: F401
from .agent import AgentLoop, RunSummary, decompose_from_dicts  # noqa: F401
