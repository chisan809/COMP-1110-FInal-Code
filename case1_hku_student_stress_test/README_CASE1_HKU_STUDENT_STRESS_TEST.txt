# Case 1: HKU Student Stress Test

## Goal
Stress-test large CSV import, many categories, multi-month reports, large one-off expenses, global limit warnings, category budget warnings, and text chart.

## Files in this folder
- `budget.py`: the program to run
- `budget_data.csv`: empty transaction file for clean testing
- `budget_categories.csv`: category storage file
- `budget_limit.txt`: global monthly limit for this case
- `category_budgets.csv`: category budget settings
- `recurring_transactions.csv`: recurring transaction file
- `rollover_balances.csv`: rollover balance file
- `scenario1_studentSpending_stressTest_transactions.csv`: main scenario CSV to import

## How to start
1. Open Terminal.
2. `cd` into this folder.
3. Run:
   `python3 budget.py`

## Demo flow
1. Choose option `6`: Import Transactions from CSV.
2. Type:
   `scenario1_studentSpending_stressTest_transactions.csv`
3. Choose option `2`: Monthly Report.
4. Select the month you want to view.
5. Explain total income, total expenses, net balance, global limit warning, category budget warnings, and text chart.
6. No recurring setup is required. Optional: import scenario1_dirty_rows_for_validation.csv to test invalid-row handling.

## Expected result summary
Global monthly limit: $11500.00
- 2026-05: income $10800.00, expenses $20807.00, net $-10007.00, limit exceeded by $9307.00
- 2026-06: income $10501.00, expenses $20333.00, net $-9832.00, limit exceeded by $8833.00
- 2026-07: income $10500.00, expenses $18808.99, net $-8308.99, limit exceeded by $7308.99

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
