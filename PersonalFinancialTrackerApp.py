import sqlite3

def connect_to_db(db_name="finance.db"):#connecting to database if it exists or creating new one.
    try:
        conn = sqlite3.connect(db_name)#creating a variable that will be connecting/openning database with"db_name" name.
        return conn
    except sqlite3.Error as e:
        print(f"Database connect error:{e}")
        return None

def create_table(conn):#this function will be creating table in my db if it does not exist and it will be skipped the table exists
    try:
        cursor = conn.cursor()
        cursor.execute('''       
        CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_type TEXT NOT NULL, 
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        description TEXT
        )''')
        conn.commit()
    except sqlite3.Error as e:
        print (f"Database table ceration error: {e}")

#This function will close the database  after creating tables or modifying tables in database
def close_db_connection(conn):
    try:
        conn.close()
    except sqlite3.Error as e:
        print (f"Database close error: {e}")


#this function will be used in creating new transactions to our database
def create_transaction(conn, transaction):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO transactions (transaction_type, amount, category, date, description)
        VALUES (?,?,?,?,?)
        ''', (transaction['transaction_type'], transaction['amount'], transaction['category'],
        transaction['date'], transaction['description']))
        conn.commit()
        return cursor.lastrowid  # Return the ID of the new transaction
    except sqlite3.Error as e:
        print(f"Error creating transaction: {e}")
        return None

#this function will be displaying the created transaction from our database
def get_all_transactions(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error getting all transactions: {e}")
        return []


#this function will be used in updating already existing transactions from our database
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
    except sqlite3.Error as e:
        print(f"Error updating transaction: {e}")
        return False

#this function will be used oin deleting the existing transaction by giving its id
def delete_transaction(conn, transaction_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting transaction: {e}")
        return False


#mukudziwa kale kt apa ndichaani ala
if __name__ == '__main__':
    conn = connect_to_db()
    if conn:
        create_table(conn)
        #new_income = {'transaction_type':'Income', 'amount':166.9, 'category' : 'salary', 'date':'2025-24-12', 'description':'MonthlyPaycheck'}
        #income_id = create_transaction(conn, new_income)
        all_transactions = get_all_transactions(conn)
        if all_transactions:
            print("\nAll Transactions:")
            for transaction in all_transactions:
                print(transaction)
        close_db_connection(conn)
        print("Database setup complete.")

