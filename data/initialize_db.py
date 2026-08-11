import os
import sqlite3

def initialize_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "database.db")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lieferverzug (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vorgangsnummer TEXT NOT NULL,
                neue_kw INTEGER NOT NULL,
                lieferverzugs_grund TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        connection.commit()
        print("Database initialized successfully!")
    except sqlite3.Error as error:
        print(f"Error talking to the database: {error}")
    finally:
        connection.close()

if __name__ == "__main__":
    initialize_database()
