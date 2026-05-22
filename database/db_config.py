import sqlite3

def get_db_connection():
    # This connects to your real-time database file
    conn = sqlite3.connect('mainframe.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    # 1. Ensure the Accounts table exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL,
            system TEXT NOT NULL
        )
    ''')
    
    # 2. Ensure the Transactions (History) table exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_account TEXT,
            to_account TEXT,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. Add your starter user if they aren't there
    conn.execute("INSERT OR IGNORE INTO accounts VALUES ('123', 'John Doe', 5000.0, 'MAINFRAME_01')")
    
    conn.commit()
    conn.close()

# THIS PART IS CRITICAL: It runs the setup when you execute the file
if __name__ == "__main__":
    init_db()
    print("SUCCESS: Real-time database and History tables are initialized!")