# Case 1: HKU Student Stress Test

## Goal
Stress-test large CSV import, many categories, multi-month reports, large one-off expenses, global limit warnings, category budget warnings, and text chart.

## Demo flow
1. Choose option `6`: Import Transactions from CSV.
2. Type:
   `scenario1_hku_student.csv`
3. Choose option `2`: Monthly Report.
4. Select the month you want to view.
5. Explain total income, total expenses, net balance, global limit warning, category budget warnings, and text chart.

## Expected result summary
Global monthly limit: $11500.00
- 2026-05: income $10800.00, expenses $20807.00, net $-10007.00, limit exceeded by $9307.00
- 2026-06: income $10501.00, expenses $20333.00, net $-9832.00, limit exceeded by $8833.00
- 2026-07: income $10500.00, expenses $18808.99, net $-8308.99, limit exceeded by $7308.99
