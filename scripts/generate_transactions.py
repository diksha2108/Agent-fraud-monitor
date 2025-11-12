# generate_transactions.py

import json
import csv
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def random_transaction(account_ids, branches, home_branch, start_date, end_date):
    """Generate a single random transaction dict."""
    tx_id = "TX" + str(uuid.uuid4()).split('-')[0].upper()
    account_id = random.choice(account_ids)
    amount = round(random.uniform(10, 50000), 2)        # amounts between $10 and $50k
    currency = "USD"
    location = random.choice(branches)
    timestamp = fake.date_time_between(start_date=start_date, end_date=end_date).isoformat()
    return {
        "id": tx_id,
        "account_id": account_id,
        "amount": amount,
        "currency": currency,
        "location": location,
        "home_branch": home_branch,
        "timestamp": timestamp
    }

def generate_dataset(
    n_rows=1000,
    n_accounts=100,
    branches=None,
    home_branch="local_branch",
    start_days_ago=30,
    end_days_ago=0,
    output_json="sample_transactions_large.json",
    output_csv=None
):
    """Generate dataset of transactions and save to JSON / optionally CSV."""
    if branches is None:
        branches = ["local_branch", "remote_branch", "foreign_branch", "international_branch", "regional_branch"]
    account_ids = [f"ACC{5000 + i}" for i in range(n_accounts)]
    start_date = datetime.utcnow() - timedelta(days=start_days_ago)
    end_date = datetime.utcnow() - timedelta(days=end_days_ago)

    data = []
    for _ in range(n_rows):
        tx = random_transaction(account_ids, branches, home_branch, start_date, end_date)
        data.append(tx)

    # Write JSON
    with open(output_json, "w", encoding="utf‑8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {n_rows} transactions to {output_json}")

    # Optionally write CSV
    if output_csv:
        keys = ["id","account_id","amount","currency","location","home_branch","timestamp"]
        with open(output_csv, "w", newline="", encoding="utf‑8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for row in data:
                writer.writerow({k: row[k] for k in keys})
        print(f"Saved {n_rows} transactions to {output_csv}")

if __name__ == "__main__":
    # Example usage
    generate_dataset(n_rows=5000, n_accounts=200, output_json="src/data/sample_transactions_large.json", output_csv="src/data/sample_transactions_large.csv")
