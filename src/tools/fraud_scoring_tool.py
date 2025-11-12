from agentic_framework import Tool
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class FraudScoringTool(Tool):
    name = "fraud_scoring"

    def run(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        try:
            amount = transaction.get("amount", 0.0)
            location = transaction.get("location", "")
            home_branch = transaction.get("home_branch", "")
            score = min(1.0, amount / 10000.0 + (location != home_branch) * 0.2)
            flagged = score > 0.75
            return {"score": score, "flagged": flagged}
        except Exception as e:
            logger.error("Error in FraudScoringTool", exc_info=True)
            return {"score": 0.0, "flagged": False}
