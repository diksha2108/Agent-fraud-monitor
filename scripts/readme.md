Explanation of transactions are generated:
Uses the faker library to generate random timestamps between a date range. 
Builds random amounts using uniform distribution (you can adjust to normal or other distributions if you prefer).
Selects random branches for location; sets home_branch constant (you could make that variable too).
Writes output to JSON (and CSV if desired) so you can ingest it into your system.
Parameters allow you to control number of accounts, rows, branches, date window, etc.\

How to use:
Install dependencies: pip install faker
Save the script (e.g., generate_transactions.py) into your project (maybe under src/utils/ or scripts/).

Run::
python generate_transactions.py
It will generate src/data/sample_transactions_large.json and src/data/sample_transactions_large.csv.
Use the generated dataset in your project for testing the agent workflows.
