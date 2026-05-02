# Case 2: Group Payment and Reimbursement

## Goal
Test shared payments, delayed reimbursements, and income-vs-expense separation.

## Files in this folder
- `budget.py`: the program to run
- `budget_data.csv`: empty transaction file for clean testing
- `budget_categories.csv`: category storage file
- `budget_limit.txt`: global monthly limit for this case
- `category_budgets.csv`: category budget settings
- `recurring_transactions.csv`: recurring transaction file
- `rollover_balances.csv`: rollover balance file
- `scenario2_group_payment_reimbursement_extended.csv`: main scenario CSV to import

## How to start
1. Open Terminal.
2. `cd` into this folder.
3. Run:
   `python3 budget.py`

## Demo flow
1. Choose option `6`: Import Transactions from CSV.
2. Type:
   `scenario2_group_payment_reimbursement_extended.csv`
3. Choose option `2`: Monthly Report.
4. Select the month you want to view.
5. Explain total income, total expenses, net balance, global limit warning, category budget warnings, and text chart.
6. Use the monthly report to show that reimbursements improve net balance but do not hide the original high spending categories.

## Expected result summary
Global monthly limit: $6000.00
- 2026-05: income $9850.00, expenses $10047.00, net $-197.00, limit exceeded by $4047.00
- 2026-06: income $10350.00, expenses $19287.00, net $-8937.00, limit exceeded by $13287.00
- 2026-07: income $8600.00, expenses $9129.00, net $-529.00, limit exceeded by $3129.00

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
