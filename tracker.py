import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# connecting to SQLite database 
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# expenses table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    date TEXT,
    amount REAL,
    category TEXT
)
''')

conn.commit()

# add a new expense
def add_expense(date, amount, category):
    cursor.execute('''
    INSERT INTO expenses (date, amount, category)
    VALUES (?, ?, ?)
    ''', (date, amount, category))
    conn.commit()
    
# show all expenses
def get_expenses():
    cursor.execute('SELECT * FROM expenses')
    return cursor.fetchall()

# show remaining budget
def calculate_remaining_budget(monthly_budget):
    cursor.execute('SELECT SUM(amount) FROM expenses')
    total_spent = cursor.fetchone()[0]
    if total_spent is None:
        total_spent = 0
    return monthly_budget - total_spent

# plot piechart
def plot_expenses():
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=['Category', 'Amount'])
        plt.figure(figsize=(8, 8))
        plt.pie(df['Amount'], labels=df['Category'], autopct='%1.1f%%', startangle=140)
        plt.title('Expenses by Category')
        plt.show()
    else:
        print("No expenses to plot.")

# clear all expenses
def remove_all_expenses():
    confirmation = input("Are you sure? (y/n): ")
    if confirmation == 'y':
        cursor.execute('DELETE FROM expenses')
        conn.commit()
        print("All records deleted succesfully!")
    else:
        print("Operation cancelled.")

# change monthly budget
def change_monthly_budget():
    global monthly_budget
    new_budget = float(input("Enter new monthly budget: "))
    monthly_budget = new_budget
    print(f"Monthly budget changed to {monthly_budget}.")

def main():
    global monthly_budget
    monthly_budget = 10000  # fixed monthly budget 
    while True:
        print("0. Change Monthly Budget")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Remaining Budget")
        print("4. Plot Expenses")
        print("5. Remove All Expenses")
        print("6. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 0:
            change_monthly_budget()
        elif choice == 1:
            date = input("Enter date (DD-MM-YYYY): ")
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            add_expense(date, amount, category)
        elif choice == 2:
            expenses = get_expenses()
            if expenses:
                for expense in expenses:
                    print(expense)
            else:
                print("No expenses to view.")
        elif choice == 3:
            remaining_budget = calculate_remaining_budget(monthly_budget)
            print(f"Remaining Budget: {remaining_budget}")
        elif choice == 4:
            plot_expenses()
        elif choice == 5:
            remove_all_expenses()
        elif choice == 6:
            break
        else:
            print("Invalid choice! Please try again.")
    
    conn.close()

if __name__ == "__main__":
    main()