import csv
import os
import sys
from datetime import datetime
from collections import defaultdict

DATA_FILE       = "budget_data.csv"
CATEGORIES_FILE = "budget_categories.csv"
LIMIT_FILE      = "budget_limit.txt"
CATEGORY_BUDGETS_FILE = "category_budgets.csv"
RECURRING_FILE = "recurring_transactions.csv"
ROLLOVER_FILE = "rollover_balances.csv"
WARNING_THRESHOLD = 0.85  # warn at 85% of limit

FIELDNAMES = ["date", "type", "category", "amount", "description"]


# ── Data I/O ──────────────────────────────────────────────────────────────────
# Read "budget_data.csv" safely and skip invalid rows
def load_transactions():
    transactions = []

    if not os.path.exists(DATA_FILE):
        return transactions

    with open(DATA_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            return transactions

        for row_number, row in enumerate(reader, start=2):
            try:
                date_str = row.get("date", "").strip()
                t_type = row.get("type", "").strip().lower()
                category = row.get("category", "").strip()
                amount_raw = row.get("amount", "").strip()
                description = row.get("description", "").strip()

                datetime.strptime(date_str, "%Y-%m-%d")

                if t_type not in ["income", "expense"]:
                    raise ValueError("type must be income or expense")

                if not category:
                    raise ValueError("missing category")

                amount = float(amount_raw)

                if amount <= 0:
                    raise ValueError("amount must be positive")

                transactions.append({
                    "date": date_str,
                    "type": t_type,
                    "category": category,
                    "amount": amount,
                    "description": description,
                })

            except Exception as e:
                print(f"  Skipping invalid saved row {row_number}: {e}")

    return transactions
    
# Write the list of transactions to "budget_data.csv"
def save_transactions(transactions):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(transactions)

# Read "budget_categories.csv" and return a list of categories
def load_categories():
    if not os.path.exists(CATEGORIES_FILE):
        return []
    with open(CATEGORIES_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

# Write the list of categories to "budget_categories.csv"
def save_categories(categories):
    with open(CATEGORIES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for cat in categories:
            writer.writerow([cat])

# Read "budget_limit.txt" and return the limit as a positive float, or None if invalid
def load_limit():
    if not os.path.exists(LIMIT_FILE):
        return None
    with open(LIMIT_FILE, encoding="utf-8") as f:
        content = f.read().strip()
        try:
            limit = float(content)
            if limit <= 0:
                return None
            return limit
        except ValueError:
            return None

# Write the limit to "budget_limit.txt"
def save_limit(limit):
    with open(LIMIT_FILE, "w", encoding="utf-8") as f:
        f.write("" if limit is None else str(limit))

# Add category-based budget file functions
def load_category_budgets():
    category_budgets = {}

    if not os.path.exists(CATEGORY_BUDGETS_FILE):
        return category_budgets

    with open(CATEGORY_BUDGETS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                category = row["category"].strip()
                budget = float(row["budget"])

                if category and budget >= 0:
                    category_budgets[category] = budget

            except Exception:
                pass

    return category_budgets


def save_category_budgets(category_budgets):
    with open(CATEGORY_BUDGETS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "budget"])
        writer.writeheader()

        for category, budget in category_budgets.items():
            writer.writerow({
                "category": category,
                "budget": budget
            })

# Add rollover budget file functions
def load_rollovers():
    rollovers = {}

    if not os.path.exists(ROLLOVER_FILE):
        return rollovers

    with open(ROLLOVER_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                month = row["month"].strip()
                category = row["category"].strip()
                rollover = float(row["rollover"])

                if month and category:
                    rollovers[(month, category)] = rollover

            except Exception:
                pass

    return rollovers


def save_rollovers(rollovers):
    with open(ROLLOVER_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["month", "category", "rollover"])
        writer.writeheader()

        for (month, category), rollover in rollovers.items():
            writer.writerow({
                "month": month,
                "category": category,
                "rollover": rollover
            })

# ── Helpers ───────────────────────────────────────────────────────────────────
# Print a separator line
def separator(char="─", width=52):
    print(char * width)

# Print a header
def header(title):
    separator("═")
    print(f"  {title}")
    separator("═")

# Prompt the user for a float value
def prompt_float(msg):
    while True:
        try:
            val = float(input(msg).strip())
            if val <= 0:
                print("  Please enter a positive number.")
                continue
            return val
        except ValueError:
            print("  Invalid number. Try again.")

# Prompt the user for a choice from a list of choices
def prompt_choice(msg, choices):
    choices_lower = [c.lower() for c in choices]
    while True:
        val = input(msg).strip().lower()
        if val in choices_lower:
            return val
        print(f"  Choose from: {', '.join(choices)}")

# Pick an existing category or create a new one
def pick_or_create_category(categories):
    """Let the user pick an existing category or create a new one."""
    if categories:
        print("  Existing categories:")
        for i, cat in enumerate(categories, 1):
            print(f"    {i}. {cat}")
        print(f"    {len(categories) + 1}. + Create new category")
        while True:
            raw = input("  Select number: ").strip()
            try:
                idx = int(raw) - 1
                if 0 <= idx < len(categories):
                    return categories[idx]
                if idx == len(categories):
                    break   # fall through to create-new
            except ValueError:
                pass
            print("  Invalid choice.")
    else:
        print("  No categories yet. Creating a new one.")

    # Create new
    while True:
        name = input("  New category name: ").strip()
        if not name:
            print("  Name cannot be empty.")
            continue
        if name in categories:
            print(f"  '{name}' already exists.")
            continue
        categories.append(name)
        save_categories(categories)
        print(f"  ✓ Category '{name}' saved.")
        return name

# Return the total expenses for a selected month in YYYY-MM format
def total_expenses_for_month(transactions, ym):
    return sum(
        t["amount"] for t in transactions
        if t["type"] == "expense" and t["date"][:7] == ym
    )

# Print warning if the global limit is exceeded or close to limit for a selected month
def check_global_limit(transactions, limit, ym=None):
    if limit is None or limit <= 0:
        return

    if ym is None:
        ym = datetime.now().strftime("%Y-%m")

    spent = total_expenses_for_month(transactions, ym)
    ratio = spent / limit

    if ratio >= 1.0:
        print(f"\n  ⚠  LIMIT EXCEEDED: Total expenses in {ym} "
              f"(${spent:.2f}) have exceeded your limit of ${limit:.2f}!")
    elif ratio >= WARNING_THRESHOLD:
        print(f"\n  ⚠  WARNING: Total expenses in {ym} are at "
              f"{ratio*100:.0f}% of your ${limit:.2f} limit "
              f"(${spent:.2f} spent)")

# Get the next month in YYYY-MM format
def get_next_month(month):
    year, month_num = map(int, month.split("-"))

    if month_num == 12:
        return f"{year + 1}-01"
    else:
        return f"{year}-{month_num + 1:02d}"

# Add the text-based expense chart function
def print_expense_chart(cat_totals, max_bar_length=30):
    if not cat_totals:
        return

    max_amount = max(cat_totals.values())
    if max_amount <= 0:
        return

    print()
    print("  Expense Chart by Category")
    separator("-", 65)

    for cat, total in sorted(cat_totals.items(), key=lambda x: -x[1]):
        bar_length = int((total / max_amount) * max_bar_length)

        if total > 0 and bar_length == 0:
            bar_length = 1

        bar = "█" * bar_length
        print(f"  {cat:<22} | {bar:<30} ${total:>9.2f}")

    separator("-", 65)

# ── Features ──────────────────────────────────────────────────────────────────
# Add a new transaction
def add_transaction(transactions, categories, limit):
    header("Add Transaction")

    t_type = prompt_choice("  Type (income/expense): ", ["income", "expense"])

    print()
    category = pick_or_create_category(categories)

    amount = prompt_float("  Amount: $")

    print("  Description (optional, press Enter to skip): ", end="")
    description = input().strip()

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n  Date options:")
    print(f"    1. Today ({today})")
    print(f"    2. Enter a custom date (format: YYYY-MM-DD)")
    date_choice = prompt_choice("  Choose (1/2): ", ["1", "2"])
    if date_choice == "1":
        date_str = today
    else:
        while True:
            raw = input("  Enter date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(raw, "%Y-%m-%d")
                date_str = raw
                break
            except ValueError:
                print("  Invalid format. Please use YYYY-MM-DD (e.g. 2026-03-15).")
    transactions.append({
        "date": date_str,
        "type": t_type,
        "category": category,
        "amount": amount,
        "description": description,
    })

    print(f"\n  ✓ Added: [{t_type.upper()}] ${amount:.2f} — {category}"
          + (f" ({description})" if description else ""))

    if t_type == "expense":
        check_global_limit(transactions, limit, date_str[:7])

# Print monthly report
def monthly_report(transactions, category_budgets, rollovers):
    header("Monthly Report")

    if not transactions:
        print("  No transactions recorded yet.\n")
        return

    months = sorted({t["date"][:7] for t in transactions}, reverse=True)

    print("  Available months:")
    for i, m in enumerate(months, 1):
        print(f"    {i}. {m}")
    print("    0. All months")

    while True:
        choice = input("\n  Select (0 / number): ").strip()
        if choice == "0":
            selected = months
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(months):
                selected = [months[idx]]
                break
        except ValueError:
            pass
        print("  Invalid choice.")

    for ym in selected:
        separator()
        print(f"  Period: {ym}")
        separator()

        month_txns = [t for t in transactions if t["date"][:7] == ym]
        income_total  = sum(t["amount"] for t in month_txns if t["type"] == "income")
        expense_total = sum(t["amount"] for t in month_txns if t["type"] == "expense")

        cat_totals = defaultdict(float)
        for t in month_txns:
            if t["type"] == "expense":
                cat_totals[t["category"]] += t["amount"]

        print(f"  {'Total Income:':<25} ${income_total:>10.2f}")
        print(f"  {'Total Expenses:':<25} ${expense_total:>10.2f}")
        print(f"  {'Net:':<25} ${income_total - expense_total:>10.2f}")

        has_rollover_for_month = any(m == ym for m, category in rollovers.keys())

        if cat_totals or category_budgets or has_rollover_for_month:
            print()
            print("  Expense by Category Budget")
            separator("-", 70)
            print(f"  {'Category':<18} {'Spent':>10} {'Budget':>12} {'Remaining':>12}")
            separator("-", 70)

            all_categories = set(cat_totals.keys()) | set(category_budgets.keys())
            for m, category in rollovers.keys():
                if m == ym:
                    all_categories.add(category)
            overspent_categories = []

            for cat in sorted(all_categories, key=lambda x: -cat_totals.get(x, 0)):
                spent = cat_totals.get(cat, 0)
                base_budget = category_budgets.get(cat)
                rollover = rollovers.get((ym, cat), 0)
                
                if base_budget is None and rollover == 0:
                    budget_text = "Not set"
                    remaining_text = "-"
                else:
                    available_budget = (base_budget or 0) + rollover
                    remaining = available_budget - spent
                    
                    if rollover == 0:
                        budget_text = f"${available_budget:.2f}"
                    else:
                        budget_text = f"${available_budget:.2f}"
                        
                    remaining_text = f"${remaining:.2f}"
                    
                    if remaining < 0:
                        overspent_categories.append((cat, abs(remaining)))

                print(f"  {cat:<18} ${spent:>9.2f} {budget_text:>12} {remaining_text:>12}")

            separator("-", 70)

            if overspent_categories:
                print()
                for cat, amount in overspent_categories:
                    print(f"  ⚠ {cat} exceeded its category budget by ${amount:.2f}")
            
            print_expense_chart(cat_totals)

        print()

# Print transaction history
def view_transactions(transactions):
    header("Transaction History")

    if not transactions:
        print("  No transactions recorded yet.\n")
        return

    print(f"  {'Date':<12} {'Type':<9} {'Category':<18} {'Amount':>9}  Description")
    separator("-", 65)
    for t in transactions:
        sign = "+" if t["type"] == "income" else "-"
        desc = t["description"][:22] if t["description"] else ""
        print(f"  {t['date']:<12} {t['type']:<9} {t['category']:<18} "
              f"{sign}${t['amount']:>8.2f}  {desc}")
    separator("-", 65)
    print(f"  Total records: {len(transactions)}\n")

# Set, update or remove the monthly limit
def manage_limit(transactions, limit_holder):
    """limit_holder is a list of one element so we can mutate it."""
    header("Budget Limit")

    current = limit_holder[0]
    ym = datetime.now().strftime("%Y-%m")
    spent = total_expenses_for_month(transactions, ym)

    if current is not None:
        ratio = spent / current
        status = f"{ratio*100:.0f}% used" if ratio < 1.0 else "EXCEEDED"
        print(f"  Current limit : ${current:.2f} / month")
        print(f"  Spent ({ym}) : ${spent:.2f}  [{status}]")
    else:
        print("  No monthly limit set.")
        print(f"  Spent ({ym}) : ${spent:.2f}")

    print()
    print("  1. Set / update limit")
    print("  2. Remove limit")
    print("  0. Back")
    choice = input("\n  Choice: ").strip()

    if choice == "1":
        val = prompt_float("  New monthly total-expense limit: $")
        limit_holder[0] = val
        save_limit(val)
        print(f"  ✓ Limit set to ${val:.2f} per month.\n")
        check_global_limit(transactions, val)

    elif choice == "2":
        limit_holder[0] = None
        save_limit(None)
        print("  ✓ Limit removed.\n")

    elif choice == "0":
        pass
    else:
        print("  Invalid option.\n")

# Add category-based budget management function
def manage_category_budgets(categories, category_budgets):
    header("Manage Category Budgets")

    while True:
        print("  Current Category Budgets")
        separator("-", 52)

        if not category_budgets:
            print("  No category budgets set yet.")
        else:
            for category, budget in category_budgets.items():
                print(f"  {category:<25} ${budget:>10.2f}")

        separator("-", 52)
        print("  1. Set / update category budget")
        print("  2. Remove category budget")
        print("  0. Back")

        choice = input("\n  Choice: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            category = pick_or_create_category(categories)
            budget = prompt_float("  Category budget amount: $")

            category_budgets[category] = budget
            save_category_budgets(category_budgets)

            print(f"  ✓ Budget for '{category}' set to ${budget:.2f}\n")

        elif choice == "2":
            if not category_budgets:
                print("  No category budgets to remove.\n")
                continue

            budget_categories = list(category_budgets.keys())

            for i, category in enumerate(budget_categories, 1):
                print(f"    {i}. {category} - ${category_budgets[category]:.2f}")

            raw = input("  Select number to remove: ").strip()

            try:
                idx = int(raw) - 1

                if 0 <= idx < len(budget_categories):
                    removed = budget_categories[idx]
                    del category_budgets[removed]
                    save_category_budgets(category_budgets)
                    print(f"  ✓ Removed budget for '{removed}'.\n")
                else:
                    print("  Invalid choice.\n")

            except ValueError:
                print("  Invalid choice.\n")

        else:
            print("  Invalid option.\n")

# View, add or delete categories
def manage_categories(categories):
    header("Manage Categories")

    while True:
        print("  1. View all categories")
        print("  2. Add new category")
        print("  3. Delete a category")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            if not categories:
                print("  No categories yet.\n")
            else:
                for i, cat in enumerate(categories, 1):
                    print(f"    {i}. {cat}")
                print()

        elif choice == "2":
            name = input("  New category name: ").strip()
            if not name:
                print("  Name cannot be empty.\n")
            elif name in categories:
                print(f"  '{name}' already exists.\n")
            else:
                categories.append(name)
                save_categories(categories)
                print(f"  ✓ '{name}' added.\n")

        elif choice == "3":
            if not categories:
                print("  No categories to delete.\n")
                continue
            for i, cat in enumerate(categories, 1):
                print(f"    {i}. {cat}")
            raw = input("  Select number to delete: ").strip()
            try:
                idx = int(raw) - 1
                if 0 <= idx < len(categories):
                    removed = categories.pop(idx)
                    save_categories(categories)
                    print(f"  ✓ '{removed}' deleted.\n")
                else:
                    print("  Invalid choice.\n")
            except ValueError:
                print("  Invalid choice.\n")

        else:
            print("  Invalid option.\n")

# the CSV import function
def import_transactions_from_csv(transactions, categories, limit):
    header("Import Transactions from CSV")

    print("  Expected CSV columns:")
    print("  date,type,category,amount,description")
    print()
    print("  Example row:")
    print("  2026-05-01,expense,Food,45,HKU canteen lunch")
    print()

    path = input("  Enter CSV file path: ").strip()
    path = path.strip('"').strip("'")

    if not path:
        print("  Import cancelled: no file path entered.\n")
        return

    if not os.path.exists(path):
        print(f"  File not found: {path}\n")
        return

    required_fields = set(FIELDNAMES)
    imported_count = 0
    skipped_rows = []
    imported_months = set()

    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                print("  Import failed: CSV file is empty or has no header row.\n")
                return

            # Strip header names so headers like "date " still work.
            actual_fields = {name.strip() for name in reader.fieldnames if name}
            missing = required_fields - actual_fields

            if missing:
                print("  Import failed: missing required column(s):")
                for field in sorted(missing):
                    print(f"    - {field}")
                print()
                return

            for row_number, original_row in enumerate(reader, start=2):
                try:
                    # Normalise row keys by stripping spaces from header names.
                    row = {
                        (key.strip() if key else key): (value if value is not None else "")
                        for key, value in original_row.items()
                    }

                    date_str = row.get("date", "").strip()
                    t_type = row.get("type", "").strip().lower()
                    category = row.get("category", "").strip()
                    amount_raw = row.get("amount", "").strip()
                    description = row.get("description", "").strip()

                    if not date_str:
                        raise ValueError("missing date")

                    datetime.strptime(date_str, "%Y-%m-%d")

                    if t_type not in ["income", "expense"]:
                        raise ValueError("type must be income or expense")

                    if not category:
                        raise ValueError("missing category")

                    amount = float(amount_raw)
                    if amount <= 0:
                        raise ValueError("amount must be positive")

                    transactions.append({
                        "date": date_str,
                        "type": t_type,
                        "category": category,
                        "amount": amount,
                        "description": description,
                    })

                    if category not in categories:
                        categories.append(category)

                    if t_type == "expense":
                        imported_months.add(date_str[:7])

                    imported_count += 1

                except Exception as e:
                    skipped_rows.append((row_number, str(e)))

    except Exception as e:
        print(f"  Import failed: {e}\n")
        return

    save_transactions(transactions)
    save_categories(categories)

    print(f"\n  ✓ Imported {imported_count} transaction(s).")

    if skipped_rows:
        print(f"  ⚠ Skipped {len(skipped_rows)} invalid row(s):")
        for row_number, reason in skipped_rows[:10]:
            print(f"    Row {row_number}: {reason}")

        if len(skipped_rows) > 10:
            print(f"    ... and {len(skipped_rows) - 10} more")

    if imported_count > 0:
        for ym in sorted(imported_months):
            check_global_limit(transactions, limit, ym)

    print()

# Add edit/delete transaction function
def manage_transactions(transactions):
    header("Manage Transactions")

    if not transactions:
        print("  No transactions recorded yet.\n")
        return

    while True:
        print("  Transactions:")
        separator("-", 80)

        for i, t in enumerate(transactions, 1):
            sign = "+" if t["type"] == "income" else "-"
            print(f"  {i}. {t['date']} | {t['type']} | {t['category']} | "
                  f"{sign}${t['amount']:.2f} | {t['description']}")

        separator("-", 80)
        print("  1. Edit transaction")
        print("  2. Delete transaction")
        print("  0. Back")

        choice = input("\n  Choice: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            raw = input("  Select transaction number to edit: ").strip()

            try:
                idx = int(raw) - 1

                if not (0 <= idx < len(transactions)):
                    print("  Invalid transaction number.\n")
                    continue

                old_t = transactions[idx]
                new_t = old_t.copy()

                print("  Press Enter to keep the current value.")

                new_date = input(f"  Date [{old_t['date']}]: ").strip()
                if new_date:
                    datetime.strptime(new_date, "%Y-%m-%d")
                    new_t["date"] = new_date

                new_type = input(f"  Type [{old_t['type']}]: ").strip().lower()
                if new_type:
                    if new_type not in ["income", "expense"]:
                        raise ValueError("type must be income or expense")
                    new_t["type"] = new_type

                new_category = input(f"  Category [{old_t['category']}]: ").strip()
                if new_category:
                    new_t["category"] = new_category

                new_amount = input(f"  Amount [{old_t['amount']}]: ").strip()
                if new_amount:
                    amount = float(new_amount)
                    if amount <= 0:
                        raise ValueError("amount must be positive")
                    new_t["amount"] = amount

                new_description = input(f"  Description [{old_t['description']}]: ").strip()
                if new_description:
                    new_t["description"] = new_description

                # Update only after all new inputs are valid.
                transactions[idx] = new_t
                save_transactions(transactions)
                print("  ✓ Transaction updated.\n")

            except ValueError as e:
                print(f"  Invalid input: {e}\n")

        elif choice == "2":
            raw = input("  Select transaction number to delete: ").strip()

            try:
                idx = int(raw) - 1

                if 0 <= idx < len(transactions):
                    removed = transactions.pop(idx)
                    save_transactions(transactions)
                    print(f"  ✓ Deleted transaction: {removed['description']}\n")
                else:
                    print("  Invalid transaction number.\n")

            except ValueError:
                print("  Invalid input.\n")

        else:
            print("  Invalid option.\n")

# Add recurring transactions for a selected month
def apply_recurring_transactions(transactions, categories, limit):
    header("Apply Recurring Transactions")

    if not os.path.exists(RECURRING_FILE):
        print("  No recurring_transactions.csv file found.\n")
        return

    month = input("  Enter month to apply recurring transactions (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("  Invalid month format. Use YYYY-MM.\n")
        return

    added_count = 0
    skipped_rows = []

    with open(RECURRING_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            print("  Recurring file is empty or missing a header row.\n")
            return

        for row_number, original_row in enumerate(reader, start=2):
            try:
                row = {
                    (key.strip() if key else key): (value if value is not None else "")
                    for key, value in original_row.items()
                }

                day = int(row["day"])
                t_type = row["type"].strip().lower()
                category = row["category"].strip()
                amount = float(row["amount"])
                description = row["description"].strip()

                date_str = f"{month}-{day:02d}"
                datetime.strptime(date_str, "%Y-%m-%d")

                if t_type not in ["income", "expense"]:
                    raise ValueError("type must be income or expense")

                if not category:
                    raise ValueError("missing category")

                if amount <= 0:
                    raise ValueError("amount must be positive")

                already_exists = any(
                    t["date"] == date_str and
                    t["type"] == t_type and
                    t["category"] == category and
                    t["amount"] == amount and
                    t["description"] == description
                    for t in transactions
                )

                if already_exists:
                    skipped_rows.append((row_number, "duplicate recurring transaction"))
                    continue

                transactions.append({
                    "date": date_str,
                    "type": t_type,
                    "category": category,
                    "amount": amount,
                    "description": description,
                })

                if category not in categories:
                    categories.append(category)

                added_count += 1

            except Exception as e:
                skipped_rows.append((row_number, str(e)))

    save_transactions(transactions)
    save_categories(categories)

    print(f"  ✓ Added {added_count} recurring transaction(s).")

    if skipped_rows:
        print(f"  ⚠ Skipped {len(skipped_rows)} recurring row(s):")
        for row_number, reason in skipped_rows[:10]:
            print(f"    Row {row_number}: {reason}")
        if len(skipped_rows) > 10:
            print(f"    ... and {len(skipped_rows) - 10} more")

    if added_count > 0:
        check_global_limit(transactions, limit, month)

    print()

# Add rollover budgeting function
def close_month_and_rollover(transactions, category_budgets, rollovers):
    header("Close Month and Rollover")

    month = input("  Enter the month to close (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("  Invalid month format. Use YYYY-MM.\n")
        return

    next_month = get_next_month(month)

    cat_totals = defaultdict(float)

    for t in transactions:
        if t["type"] == "expense" and t["date"][:7] == month:
            cat_totals[t["category"]] += t["amount"]

    all_categories = set(category_budgets.keys()) | set(cat_totals.keys())

    for m, category in rollovers.keys():
        if m == month:
            all_categories.add(category)

    if not all_categories:
        print("  No category budgets or expenses found for this month.\n")
        return

    print()
    print(f"  Closing month: {month}")
    print(f"  Rollover will be applied to: {next_month}")
    separator("-", 80)
    print(f"  {'Category':<18} {'Budget':>10} {'Old Roll':>10} {'Spent':>10} {'New Roll':>10}")
    separator("-", 80)

    for category in sorted(all_categories):
        base_budget = category_budgets.get(category, 0)
        old_rollover = rollovers.get((month, category), 0)
        available = base_budget + old_rollover
        spent = cat_totals.get(category, 0)

        new_rollover = available - spent

        rollovers[(next_month, category)] = new_rollover

        print(f"  {category:<18} ${base_budget:>9.2f} ${old_rollover:>9.2f} "
              f"${spent:>9.2f} ${new_rollover:>9.2f}")

    separator("-", 80)

    save_rollovers(rollovers)

    print(f"\n  ✓ Rollover balances saved for {next_month}.\n")


# ── Main ──────────────────────────────────────────────────────────────────────

# The primary loop
def main():
    transactions = load_transactions()
    categories   = load_categories()
    limit_holder = [load_limit()]   # mutable wrapper
    category_budgets = load_category_budgets()
    rollovers = load_rollovers()

    header("Personal Budget Tracker")
    print(f"  Loaded {len(transactions)} transaction(s).")

    # Startup limit alert
    if limit_holder[0] is not None:
        check_global_limit(transactions, limit_holder[0])
    print()

    while True:
        separator("═")
        print("  MAIN MENU")
        separator("─")
        print("  1. Add Transaction")
        print("  2. Monthly Report")
        print("  3. View All Transactions")
        print("  4. Manage Budget Limit")
        print("  5. Manage Categories")
        print("  6. Import Transactions from CSV")
        print("  7. Manage Category Budgets")
        print("  8. Edit/Delete Transactions")
        print("  9. Apply Recurring Transactions")
        print("  10. Close Month and Rollover")
        print("  0. Exit")
        separator("═")
        choice = input("  Choice: ").strip()

        if choice == "0":
            save_transactions(transactions)
            print("\n  Data saved. Goodbye!\n")
            sys.exit(0)
        elif choice == "1":
            print()
            add_transaction(transactions, categories, limit_holder[0])
        elif choice == "2":
            print()
            monthly_report(transactions, category_budgets, rollovers)
        elif choice == "3":
            print()
            view_transactions(transactions)
        elif choice == "4":
            print()
            manage_limit(transactions, limit_holder)
        elif choice == "5":
            print()
            manage_categories(categories)
        elif choice == "6":
            print()
            import_transactions_from_csv(transactions, categories, limit_holder[0])
        elif choice == "7":
            print()
            manage_category_budgets(categories, category_budgets)
        elif choice == "8":
            print()
            manage_transactions(transactions)
        elif choice == "9":
            print()
            apply_recurring_transactions(transactions, categories, limit_holder[0])
        elif choice == "10":
            print()
            close_month_and_rollover(transactions, category_budgets, rollovers)
        else:
            print("  Invalid option. Try again.\n")


if __name__ == "__main__":
    main()
