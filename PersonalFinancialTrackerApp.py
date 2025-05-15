import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

#this function will help in connecting and openning my database if it exists, if it does not then the system will attempt to create one
def connect_to_db(db_name="finance.db"):
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

#this function attempts to create a table called transaction in my database if it does not exist ese it will skip
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_type TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT
        )
            ''')
        conn.commit()
    except sqlite3.Error as e:#will display an error if the table creation fails
        print(f"Database table creation error: {e}")

#this function will be called when athe user is attempting to create a transaction into our tabe called "transactions"
def create_transaction(conn, transaction):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO transactions (transaction_type, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
        ''', (transaction['transaction_type'], transaction['amount'], transaction['category'], transaction['date'], transaction['description']))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:#will display an errow if the transaction creation fails
        print(f"Error creating transaction: {e}")
        return None

#this function will be called when the user wants to display all transactions in their table
def get_all_transactions(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        return cursor.fetchall()

    except sqlite3.Error as e:#an error will be dispayed if the system fails to display the transactions
        print(f"Error getting all transactions: {e}")
        return []

#this one will be used to update existing transactions in the table by selecting one using its ID
def update_transaction(conn, transaction_id, transaction):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE transactions
        SET transaction_type = ?, amount = ?, category = ?, date = ?, description = ?
        WHERE id = ?
        ''', (transaction['transaction_type'], transaction['amount'], transaction['category'],
        transaction['date'], transaction['description'], transaction_id))
        conn.commit()
        return True
    except sqlite3.Error as e:#an error will be displayed if the system fails to get the selected transaction
        print(f"Error updating transaction: {e}")
        return False

#this function will be used in deleting transaction using selection as well
def delete_transaction(conn, transaction_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:#an error wil be displayed if the system fails to delete the transaction from our table
        print(f"Error deleting transaction: {e}")
        return False

#this function will be used to close the database after using it to avoid unintentional configurations to our database
def close_db_connection(conn):
    try:
        conn.close()
    except sqlite3.Error as e:#an error will be displayed if the system fails to close the database
        print(f"Database close error: {e}")

#adding the new functions in our database that will be used to return the total amount of a transaction in a loop
def get_total_income(conn):#This function is for calculating the total amount of the income
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'Income'")
        result = cursor.fetchone()
        if result and result[0] is not None:  # Check for None result
            return result[0]
        else:
            return 0.0  # Return 0.0 if there's no income
    except sqlite3.Error as e:#an error will be displayed the system fails to make the calcultions of the income
        print(f"Error getting total income: {e}")
        return 0.0



def get_total_expenses(conn):# this one will be used in calculating the total outcome
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'Expense'")
        result = cursor.fetchone()
        if result and result[0] is not None:  # Check for None result
            return result[0]
        else:
            return 0.0  # Return 0.0 if there are no expenses
    except sqlite3.Error as e:#an error will be displayed if the system fails to get the total amount of the outcome money
        print(f"Error getting total expenses: {e}")
    return 0.0

#the following class will be used to configure everything about the GUI and connecting to the app using Tkinter as my GUI library
class FinanceTrackerApp:
    def __init__(self, window):#creating the constructor of our main window
        self.window = window #declairing our window as window

        self.window.title("Personal Finance Tracker")

        self.conn = connect_to_db() #in my window, i'm trying to connect to the database so that I should be interacting with it
        if not self.conn:# declairing a condition if the connection with database fails that it should displlay the error in the message box
            messagebox.showerror("Error", "Sorry! the system could not connect to the database.")
            self.window.destroy()
            return

        create_table(self.conn) #creating a widget that will be used as my table for displaying transaction from my database

        self.create_widgets() #creating a widget that will be on top of the displaying widget which will be used to crete new transactions
        self.load_transactions() #this widget will be connected tho "create_table" widget for getting transactions from our database to main window
        self.create_summary_widgets()
        self.load_transactions()
        self.update_summary_labels()  # this function will be called for the transactions sumary

    def create_summary_widgets(self):

        summary_frame = ttk.LabelFrame(self.window, text="Transaction Summary")
        summary_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(summary_frame, text="Total Income:").grid(row=0, column=0, padx=5, pady=5,sticky="w")
        self.total_income_label = ttk.Label(summary_frame, text="0.00")
        self.total_income_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(summary_frame, text="Total Expenses:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.total_expenses_label = ttk.Label(summary_frame, text="0.00")
        self.total_expenses_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(summary_frame, text="Current Balance:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.current_balance_label = ttk.Label(summary_frame, text="0.00")
        self.current_balance_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def update_summary_labels(self):

        total_income = get_total_income(self.conn)
        total_expenses = get_total_expenses(self.conn)
        current_balance = total_income - total_expenses

        self.total_income_label.config(text=f"{total_income:.2f}")
        self.total_expenses_label.config(text=f"{total_expenses:.2f}")
        self.current_balance_label.config(text=f"{current_balance:.2f}")

    def add_transaction(self):
        self.update_summary_labels()  # Update summaries after adding

    def update_selected_transaction(self):
        self.update_summary_labels()  # Update summaries after updating

    def delete_selected_transaction(self):
        self.update_summary_labels()  # Update summaries after deleting

    def load_transactions(self):
        self.update_summary_labels()  # Update summaries after loading


#this fuction creates labels and input fields for creating new transsactions
    def create_widgets(self):


        input_frame = ttk.LabelFrame(self.window, text="Enter Transaction")
        input_frame.pack(padx=10, pady=10)

        ttk.Label(input_frame, text="Type (Income/Expense):").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar()
        ttk.Combobox(input_frame, textvariable=self.type_var, values=["Income", "Expense"]).grid(row=0, column=1, padx=5,
                                                                                                 pady=5)

        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(input_frame)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Date (DD/MM/YYYY):").grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=4, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(input_frame)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(input_frame, text="Add Transaction", command=self.add_transaction)
        add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

#here is a transaction table to be displayed in a tree form
        self.tree = ttk.Treeview(self.window, columns=("ID", "Type", "Amount", "Category", "Date", "Description"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Description", text="Description")
        self.tree.pack(padx=10, pady=10)

#here are the buttons that will be used in for update and delete
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Update Transaction", command=self.update_selected_transaction).pack(side=tk.LEFT,padx=5)
        ttk.Button(button_frame, text="Delete Transaction", command=self.delete_selected_transaction).pack(side=tk.LEFT,padx=5)

#this function will be used as a saving fuction that will be copying what is in the entry fields in GUI and then sending them to my database's table
    def add_transaction(self):
        try:
            transaction_type = self.type_var.get()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            date = self.date_entry.get()
            description = self.description_entry.get()

            if not transaction_type or not category or not date:#declairing a condition that will be triggered to display an error if the user fails to provide the required information
                raise ValueError("Type, category, and date are required.")
            transaction = {
                    'transaction_type': transaction_type,
                    'amount': amount,
                    'category': category,
                    'date': date,
                    'description': description
                } #otherwise the system will create the transaction if the requirements are fulfilled

            transaction_id = create_transaction(self.conn, transaction)
            if transaction_id:#upon a successful creation of the traansaction, the system will clear the displaying field and refreshes with the newly created transaction
                self.load_transactions()
                self.clear_input_fields()
                messagebox.showinfo("Success", "Transaction added.")
            else:#an error will be displayed if the system fails to refresh the displaying table
                messagebox.showerror("Error", "Failed to add transaction.")

        except ValueError as e:#an error will be displayed if the system fails to paste the coppied info to the database
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

#this function is to be used in displaying the transactions that are in the table
    def load_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        transactions = get_all_transactions(self.conn)
        for transaction in transactions:
            self.tree.insert("", tk.END, values=transaction)

#this fuction will be used to clear the input fileds for next new transaction upon a successful transaction
    def clear_input_fields(self):
        self.type_var.set("")
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

#this function will be used to select a transaction from out displaying tree table
    def get_selected_transaction_id(self):
        selected_item = self.tree.selection()

        if not selected_item:#an error will be displayed if the selection fails
            messagebox.showerror("Error", "No transaction selected.")
            return None
        return self.tree.item(selected_item[0])['values'][0]

#tis fuction will be called upon clicking the update button for update
    def update_selected_transaction(self):
        transaction_id = self.get_selected_transaction_id()

        if not transaction_id:
            return

        try:
            transaction_type = self.type_var.get()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            date = self.date_entry.get()
            description = self.description_entry.get()

            if not transaction_type or not category or not date:
                raise ValueError("Type, category, and date are required.")

            transaction = {
                'transaction_type': transaction_type,
                'amount': amount,
                'category': category,
                'date': date,
                'description': description
            }

            if update_transaction(self.conn, transaction_id, transaction):
                self.load_transactions()
                self.clear_input_fields()
                messagebox.showinfo("Success", "Transaction updated.")
            else:
                messagebox.showerror("Error", "Failed to update transaction.")


        except ValueError as e:#an error will be displayed if the system fails to update the selected trans
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

#this function will be used to delete a transaction from our table in the database
    def delete_selected_transaction(self):
        transaction_id = self.get_selected_transaction_id()

        if not transaction_id:
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this transaction?"): #asking the user for the comfirmation
            if delete_transaction(self.conn, transaction_id):
                self.load_transactions()
                messagebox.showinfo("Success", "Transaction deleted.")
            else:#an error will be displayed if the system fails to dalete a transaction
                messagebox.showerror("Error", "Failed to delete transaction.")


#this function is declairing and initializing the window (main window)
def main():
    window = tk.Tk() #initializing the window as window in tkinter
    app = FinanceTrackerApp(window)
    window.mainloop() #openning a loop of the window so that it does not close as soon we open it

if __name__ == '__main__':#running directly to the main window
    main()
