import csv
import os
from datetime import datetime
from collections import defaultdict

FILE_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "expenses.csv"
)

FIELDS = ["ID", "Date", "Category", "Description", "Amount"]


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()


def load_expenses():
    initialize_file()

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def save_expenses(expenses):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def get_next_id(expenses):
    if not expenses:
        return 1

    return max(int(expense["ID"]) for expense in expenses) + 1


def add_expense():
    expenses = load_expenses()

    print("\n--- Add New Expense ---")

    while True:
        date_input = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        ).strip()

        if not date_input:
            expense_date = datetime.today().strftime("%Y-%m-%d")
            break

        try:
            expense_date = datetime.strptime(
                date_input, "%Y-%m-%d"
            ).strftime("%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Example: 2026-10-14")

    category = input(
        "Enter category (Food, Travel, Shopping, Bills, Other): "
    ).strip()

    while not category:
        category = input(
            "Category cannot be empty. Enter category: "
        ).strip()

    description = input("Enter description: ").strip()

    while True:
        try:
            amount = float(input("Enter amount (₹): "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            if not amount < float("inf"):
                print("Please enter a valid finite amount.")
                continue

            break
        except ValueError:
            print("Please enter a valid number.")

    new_expense = {
        "ID": str(get_next_id(expenses)),
        "Date": expense_date,
        "Category": category.title(),
        "Description": description,
        "Amount": f"{amount:.2f}"
    }

    expenses.append(new_expense)
    save_expenses(expenses)

    print("\nExpense added successfully!")
    print(f"Expense ID: {new_expense['ID']}")
    print(f"Amount: ₹{amount:.2f}")


def view_expenses():
    expenses = load_expenses()

    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    print("-" * 85)
    print(
        f"{'ID':<5}{'Date':<13}{'Category':<16}"
        f"{'Description':<27}{'Amount (₹)':>15}"
    )
    print("-" * 85)

    for expense in expenses:
        print(
            f"{expense['ID']:<5}"
            f"{expense['Date']:<13}"
            f"{expense['Category']:<16}"
            f"{expense['Description'][:25]:<27}"
            f"{float(expense['Amount']):>15.2f}"
        )

    print("-" * 85)


def show_total():
    expenses = load_expenses()

    total = sum(float(expense["Amount"]) for expense in expenses)

    print("\n--- Total Spending ---")
    print(f"Number of expenses: {len(expenses)}")
    print(f"Total amount spent: ₹{total:.2f}")


def category_summary():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available for summary.")
        return

    totals = defaultdict(float)

    for expense in expenses:
        totals[expense["Category"]] += float(expense["Amount"])

    grand_total = sum(totals.values())

    print("\n--- Category-wise Spending ---")

    for category, amount in sorted(totals.items()):
        percentage = amount / grand_total * 100
        print(f"{category:<20} ₹{amount:>10.2f} ({percentage:.1f}%)")

    print("-" * 45)
    print(f"{'Grand Total':<20} ₹{grand_total:>10.2f}")


def search_by_date():
    expenses = load_expenses()

    try:
        search_date = datetime.strptime(
            input("\nEnter date (YYYY-MM-DD): ").strip(),
            "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    results = [
        expense for expense in expenses
        if expense["Date"] == search_date
    ]

    if not results:
        print("No expenses found for this date.")
        return

    print(f"\nExpenses on {search_date}:")

    for expense in results:
        print(
            f"ID: {expense['ID']} | "
            f"{expense['Category']} | "
            f"{expense['Description']} | "
            f"₹{float(expense['Amount']):.2f}"
        )

    total = sum(float(expense["Amount"]) for expense in results)
    print(f"Total for {search_date}: ₹{total:.2f}")


def delete_expense():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available to delete.")
        return

    view_expenses()

    expense_id = input("\nEnter the ID to delete: ").strip()

    matching = [
        expense for expense in expenses
        if expense["ID"] == expense_id
    ]

    if not matching:
        print("Expense ID not found.")
        return

    confirm = input(
        f"Delete expense ID {expense_id}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        expenses = [
            expense for expense in expenses
            if expense["ID"] != expense_id
        ]
        save_expenses(expenses)
        print("Expense deleted successfully.")
    else:
        print("Deletion cancelled.")


def main():
    initialize_file()

    while True:
        print("\n========== PERSONAL EXPENSE TRACKER ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Total Spending")
        print("4. Category-wise Summary")
        print("5. Search Expenses by Date")
        print("6. Delete Expense")
        print("7. Exit")
        print("===============================================")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_total()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            search_by_date()
        elif choice == "6":
            delete_expense()
        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1 to 7.")


if __name__ == "__main__":
    main()
