import sqlite3

class AccountService:
    def __init__(self, db_path='mainframe.db'):
        self.db_path = db_path

    def get_all_accounts(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        accounts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return accounts

    def create_new_account(self, id, name, balance, system):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("INSERT INTO accounts (id, name, balance, system) VALUES (?, ?, ?, ?)", 
                         (id, name, balance, system))
            conn.commit()
            return {"status": "success"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def transfer_funds(self, from_id, to_id, amount):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            # Deduct from sender
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
            # Add to recipient
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
            # Log the transaction
            cursor.execute("INSERT INTO transactions (from_account, to_account, amount) VALUES (?, ?, ?)", 
                           (from_id, to_id, amount))
            conn.commit()
            return {"status": "success"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def get_transaction_history(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY timestamp DESC")
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return history