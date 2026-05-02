# Case 4: Travel Preparation and Rollover Budgeting

## Goal
Test large travel expenses, recurring transactions, and rollover budgeting where May balances affect June budgets.

## Demo flow
1. Choose option `6`: Import Transactions from CSV.
2. Type:
   `scenario4_travel.csv`
3. Choose option `2`: Monthly Report.
4. Select the month you want to view.
5. Explain total income, total expenses, net balance, global limit warning, category budget warnings, and text chart.
6. After importing the CSV, apply recurring transactions for 2026-05. Then choose option 10 and close 2026-05. Generate the 2026-06 report for the rollover effect. You may also apply recurring transactions for 2026-06.

## Expected result summary
Global monthly limit: $13000.00
- 2026-05: income $12600.00, expenses $20574.00, net $-7974.00, limit exceeded by $7574.00
- 2026-06: income $12900.00, expenses $17649.00, net $-4749.00, limit exceeded by $4649.00

- Recurring applied to 2026-05: added 4, skipped 1
- Recurring applied to 2026-06: added 4, skipped 1
