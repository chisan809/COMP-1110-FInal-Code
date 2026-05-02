# Case 2: Group Payment and Reimbursement

## Goal
Test shared payments, delayed reimbursements, and income-vs-expense separation.

## flow
1. Choose option `6`: Import Transactions from CSV.
2. Type:
   `scenario2_groupPayment.csv`
3. Choose option `2`: Monthly Report.
4. Select the month you want to view.
5. Explain total income, total expenses, net balance, global limit warning, category budget warnings, and text chart.
6. Use the monthly report to show that reimbursements improve net balance but do not hide the original high spending categories.

## Expected result summary
Global monthly limit: $6000.00
- 2026-05: income $9850.00, expenses $10047.00, net $-197.00, limit exceeded by $4047.00
- 2026-06: income $10350.00, expenses $19287.00, net $-8937.00, limit exceeded by $13287.00
- 2026-07: income $8600.00, expenses $9129.00, net $-529.00, limit exceeded by $3129.00
