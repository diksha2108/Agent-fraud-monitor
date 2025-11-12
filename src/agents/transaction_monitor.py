# src/agents/transaction_monitor.py

import logging
from typing import Dict, Any

from agentic_framework import Agent

from src.tools.fraud_scoring_tool import FraudScoringTool
from src.tools.account_action_tool import AccountActionTool
from src.tools.audit_log_tool import AuditLogTool

logger = logging.getLogger(__name__)

class TransactionMonitorAgent:
    """
    Agent to monitor financial transactions, assess fraud risk, and take appropriate
    action (freeze, escalate, or approve), while maintaining audit logs.
    """

    @staticmethod
    def create_agent(model: str = "openai/gpt‑4", 
                     freeze_threshold: float = 0.9,
                     escalate_threshold: float = 0.75) -> Agent:
        """
        Factory method to create the Agentic agent with proper instructions and tools.
        :param model: The LLM model to use.
        :param freeze_threshold: Score above which account is frozen.
        :param escalate_threshold: Score above which but below freeze_threshold => escalate.
        :return: Configured Agent instance.
        """
        instructions = f"""
You are a transaction monitoring agent. For each incoming transaction you must:
1. Use the fraud_scoring tool to compute a risk score.
2. Based on the score:
   - If score >= {freeze_threshold} → freeze the account immediately.
   - If {escalate_threshold} < score < {freeze_threshold} → escalate to human compliance review.
   - Otherwise (score <= {escalate_threshold}) → approve/clear the transaction.
3. Use the account_action tool to perform the action (freeze, escalate, approve) with account_id and reason.
4. Use the audit_log tool to record the following:
   - transaction_id
   - account_id
   - received_at timestamp
   - risk_score
   - flagged (True/False)
   - action_taken
   - reason
Return a JSON object with keys:
  transaction_id, score, flagged, action_taken, reason
Only use the provided tools.
"""
        return Agent(
            name="TransactionMonitorAgent",
            instructions=instructions,
            tools=[FraudScoringTool(), AccountActionTool(), AuditLogTool()],
            model=model
        )

    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def process_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single transaction through the agent.
        :param transaction: dictionary with transaction fields (id, account_id, amount, etc.).
        :return: decision dictionary from agent.
        """
        logger.info(f"Processing transaction {transaction.get('id')} for account {transaction.get('account_id')}")
        # Enrich with metadata
        transaction["received_at"] = transaction.get("received_at") or ""
        transaction["request_id"] = transaction.get("request_id") or ""
        prompt = f"""Transaction received: {transaction}
Please analyse and respond with a JSON‐structured decision."""
        try:
            response = self.agent.run(prompt)
            logger.info(f"Agent response for transaction {transaction.get('id')}: {response}")
            return response
        except Exception as e:
            logger.error(f"Error executing agent for transaction {transaction.get('id')}: {e}", exc_info=True)
            # Fallback decision
            fallback = {
                "transaction_id": transaction.get("id"),
                "score": None,
                "flagged": True,
                "action_taken": "escalate",
                "reason": "agent_error_fallback"
            }
            logger.info(f"Fallback decision: {fallback}")
            return fallback
