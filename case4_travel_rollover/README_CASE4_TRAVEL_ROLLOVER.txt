# Case 4: Travel Preparation and Rollover Budgeting

## Goal
Test large travel expenses, recurring transactions, and rollover budgeting where May balances affect June budgets.

## Files in this folder
- `budget.py`: the program to run
- `budget_data.csv`: empty transaction file for clean testing
- `budget_categories.csv`: category storage file
- `budget_limit.txt`: global monthly limit for this case
- `category_budgets.csv`: category budget settings
- `recurring_transactions.csv`: recurring transaction file
- `rollover_balances.csv`: rollover balance file
- `scenario4_travel_rollover_extended.csv`: main scenario CSV to import

## How to start
1. Open Terminal.
2. `cd` into this folder.
3. Run:
   `python3 budget.py`

## Demo flow
1. Choose option `6`: Import Transactions from CSV.
2. Type:
   `scenario4_travel_rollover_extended.csv`
3. Choose option `2`: Monthly Report.
4. Select the month you want to view.
5. Explain total income, total expenses, net balance, global limit warning, category budget warnings, and text chart.
6. After importing the CSV, apply recurring transactions for 2026-05. Then choose option 10 and close 2026-05. Generate the 2026-06 report to check the rollover effect. You may also apply recurring transactions for 2026-06.

## Expected result summary
Global monthly limit: $13000.00
- 2026-05: income $12600.00, expenses $20574.00, net $-7974.00, limit exceeded by $7574.00
- 2026-06: income $12900.00, expenses $17649.00, net $-4749.00, limit exceeded by $4649.00

- Recurring applied to 2026-05: added 4, skipped 1
- Recurring applied to 2026-06: added 4, skipped 1

## How the program is functional in this demo
- CSV import lets the user add many transactions at once.
- Monthly report calculates income, expenses, net balance, category spending, and warnings.
- Global budget limit checks whether total monthly expenses exceed the limit.
- Category budgets work like envelope budgeting.
- Text chart makes the terminal report easier to understand.
- Recurring transactions and rollover budgeting can be tested where relevant.

## Reminder
If you import the same CSV twice, duplicate transactions may appear. Reset `budget_data.csv` to only:
`date,type,category,amount,description`
before testing again.
