import os
import sqlite3

def get_every_lieferverzug():
    db_path = os.path.join("data", "database.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT vorgangsnummer, neue_kw, lieferverzugs_grund FROM lieferverzug;")
        fetched = cursor.fetchall()
        # get column names from cursor description and map each row to a dict
        columns = [col[0] for col in cursor.description] if cursor.description else []
        rows = [dict(zip(columns, row)) for row in fetched]
        return rows
    except sqlite3.Error as error:
        print(f"Error talking to the database: {error}")
        return []
    finally:
        connection.close()

def insert_lieferverzug(vorgangsnummer, neue_kw, lieferverzugs_grund):
    db_path = os.path.join("data", "database.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
        INSERT INTO lieferverzug (vorgangsnummer, neue_kw, lieferverzugs_grund)
        VALUES (?, ?, ?)
        ON CONFLICT(vorgangsnummer) DO UPDATE SET
            neue_kw = excluded.neue_kw,
            lieferverzugs_grund = excluded.lieferverzugs_grund
        """, (vorgangsnummer, neue_kw, lieferverzugs_grund)
        )
        connection.commit()
    except sqlite3.Error as error:
        print(f"Error talking to the database: {error}")
    finally:
        connection.close()

if __name__ == "__main__":
    all_lieferverzuege = get_every_lieferverzug()
    for lieferverzug in all_lieferverzuege:
        print(lieferverzug)