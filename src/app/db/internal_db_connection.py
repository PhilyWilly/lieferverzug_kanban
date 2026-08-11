import os
import aiosqlite

async def get_every_lieferverzug():
    db_path = os.path.join("data", "database.db")
    try:
        async with aiosqlite.connect(db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
        SELECT 
            vorgangsnummer, 
            MAX(neue_kw) as neue_kw, 
            lieferverzugs_grund 
        FROM lieferverzug
        GROUP BY vorgangsnummer
        ;""")
            fetched = await cursor.fetchall()
            # Convert rows to dictionaries
            rows = [dict(row) for row in fetched]
            return rows
    except aiosqlite.Error as error:
        print(f"Error talking to the database: {error}")
        return []

async def insert_lieferverzug(vorgangsnummer, neue_kw, lieferverzugs_grund):
    db_path = os.path.join("data", "database.db")
    try:
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                """
        INSERT INTO lieferverzug (vorgangsnummer, neue_kw, lieferverzugs_grund)
        VALUES (?, ?, ?)
        """, (vorgangsnummer, neue_kw, lieferverzugs_grund)
            )
            await db.commit()
    except aiosqlite.Error as error:
        print(f"Error talking to the database: {error}")

if __name__ == "__main__":
    all_lieferverzuege = get_every_lieferverzug()
    for lieferverzug in all_lieferverzuege:
        print(lieferverzug)