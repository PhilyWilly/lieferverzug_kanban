"""
Connect to the erp2crm MySQL/MariaDB database.

Setup:
    pip install aiomysql python-dotenv

.env file (same folder or a parent folder), adjust keys to match what
you actually have — rename these to match your existing .env:

    DB_HOST=192.168.216.16
    DB_PORT=3306
    DB_USER=your_username
    DB_PASSWORD=your_password
    DB_NAME=erp2crm
"""

from datetime import datetime
import os
from dotenv import load_dotenv
import aiomysql
import time

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "connect_timeout": 5,
}

async def execute_query(query, as_dict=True):
    try:
        conn = await aiomysql.connect(**config)
        cursor = await conn.cursor(aiomysql.DictCursor if as_dict else aiomysql.Cursor)
        await cursor.execute(query)
        result = await cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print("Query execution failed:", e)
        return None

async def get_mail_for_vorgangsnummer(vorgangsnummer):
    new_query = f"""SELECT
    k.email
FROM produktionslinie p

-- 1. Matches idx_prod_grouping (vp_id, vo_id, id) perfectly. 
-- The database resolves this entirely in the index tree.
INNER JOIN (
    SELECT MAX(p2.id) AS max_id
    FROM produktionslinie p2
    WHERE p2.vo_nummer = "{vorgangsnummer}"
    GROUP BY p2.vp_id, p2.vo_id
) lp ON p.id = lp.max_id

-- 2. Uses kunden_KU_NR_IDX to instantly pinpoint rows.
LEFT JOIN kunden k 
    ON p.ku_nr = k.KU_NR 
   AND k.Firma <> ''
   AND k.zeitpunkt = (
        SELECT MAX(k2.zeitpunkt)
        FROM kunden k2
        WHERE k2.KU_NR = p.ku_nr
          AND k2.Firma <> ''
   )

-- 3. Matches idx_prod_status_line (vp_delete, vo_status, produktionslinie) 
-- exactly in order, allowing a swift, direct range scan.
WHERE p.vp_delete = 0
  AND p.vo_status = 2
  AND p.produktionslinie LIKE 'Fahrgestelle%'
  AND p.vo_nummer = "{vorgangsnummer}"

ORDER BY p.vp_lieferdatum ASC, p.vo_nummer ASC
LIMIT 1;"""
    result = await execute_query(new_query, as_dict=False)
    if result:
        result = [row[0] for row in result if row[0]]  # Extract email addresses
        return result[0] if result else None
    return None

async def get_interesting_produktionslinien(department):
    query = f"""
    SELECT
    p.*,
    k.Firma  AS firma,
    k.Firma2 AS firma2,
    k.Ort    AS ort,
    k.email  AS email
FROM produktionslinie p
LEFT JOIN kunden k
    ON k.kundenid = (
        SELECT kundenid
        FROM kunden
        WHERE KU_NR = p.ku_nr
          AND Firma <> ''
        ORDER BY zeitpunkt DESC
        LIMIT 1
    )
WHERE p.vp_delete = 0
  AND p.vo_status = 2
  AND p.vo_nummer NOT LIKE 'AN%'
  AND p.produktionslinie LIKE '{department}%'
  AND p.id IN (
      SELECT MAX(id)
      FROM produktionslinie
      WHERE vo_nummer NOT LIKE 'AN%'
      GROUP BY vp_id, vo_id
  )
ORDER BY p.vp_lieferdatum, p.vo_nummer;"""
    start_time = time.time()
    result = await execute_query(query, as_dict=True)
    print(f"Query executed in {time.time() - start_time:.2f} seconds. Rows fetched: {len(result) if result else 0}")
    if not result:
        return None
    return sanitize_produktionslinien(result)

def sanitize_produktionslinien(produktionslinien):
    if not produktionslinien:
        return []
    sanitized = []
    for row in produktionslinien:
        sanitized_row = {
            "jahr": row.get("vp_liefer_kwj", None),
            "kw": row.get("vp_liefer_kw", None),
            "kundenname": row.get("firma", None),
            "vorgangsnummer": row.get("vo_nummer", None),
            "vorgangstext": row.get("vorgang_text", None),
            "artikelbeschreibung": row.get("beschreibung_kurz", None),
            "artikelnr": row.get("ar_nr", None),
            "email": row.get("email", None)
        }
        sanitized.append(sanitized_row)
    return sanitized