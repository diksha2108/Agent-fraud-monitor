# src/__init__.py

"""
agentic_fraud_monitor
---------------------
Agentic AI solution for fraud‑monitoring and workflow automation in financial institutions.
"""

__version__ = "0.1.0"

# Expose key classes at package level for convenience
from .tools.fraud_scoring_tool import FraudScoringTool
from .tools.account_action_tool import AccountActionTool
from .tools.audit_log_tool import AuditLogTool

from .agents.transaction_monitor import TransactionMonitorAgent

__all__ = [
    "FraudScoringTool",
    "AccountActionTool",
    "AuditLogTool",
    "TransactionMonitorAgent",
    "__version__"
]
