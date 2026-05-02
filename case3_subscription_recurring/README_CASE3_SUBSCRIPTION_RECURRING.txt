# Case 3: Subscription Creep and Recurring Transactions

## Goal
Test recurring transactions, duplicate recurring prevention, subscription creep, global limit warnings, and rollover after recurring payments.

## Files in this folder
- `budget.py`: the program to run
- `budget_data.csv`: empty transaction file for clean testing
- `budget_categories.csv`: category storage file
- `budget_limit.txt`: global monthly limit for this case
- `category_budgets.csv`: category budget settings
- `recurring_transactions.csv`: recurring transaction file
- `rollover_balances.csv`: rollover balance file
- `scenario3_subscription_base_extended.csv`: main scenario CSV to import

## How to start
1. Open Terminal.
2. `cd` into this folder.
3. Run:
   `python3 budget.py`

## Demo flow
1. Choose option `6`: Import Transactions from CSV.
2. Type:
   `scenario3_subscription_base_extended.csv`
3. Choose option `2`: Monthly Report.
4. Select the month you want to view.
5. Explain total income, total expenses, net balance, global limit warning, category budget warnings, and text chart.
6. After importing the base CSV, choose option 9 and apply recurring transactions for 2026-05 and 2026-06. Apply 2026-05 twice to check duplicate skipping. Then choose option 10 and close 2026-05 to test rollover.

## Expected result summary
Global monthly limit: $7600.00
- 2026-05: income $9700.00, expenses $10397.00, net $-697.00, limit exceeded by $2797.00
- 2026-06: income $9700.00, expenses $11018.00, net $-1318.00, limit exceeded by $3418.00

- Recurring applied to 2026-05: added 8, skipped 0
- Recurring applied to 2026-06: added 8, skipped 0

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
