from src.utils.logging_config import configure_logging
from src.agents.transaction_monitor import TransactionMonitorAgent
import json

def main():
    configure_logging()
    agent = TransactionMonitorAgent.create_agent()
    with open("src/data/sample_transactions.json") as f:
        txs = json.load(f)
    for tx in txs:
        decision = agent.process_transaction(tx)
        print("Decision:", decision)

if __name__ == "__main__":
    main()
