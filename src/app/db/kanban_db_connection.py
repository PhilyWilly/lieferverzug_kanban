"""
Connect to the erp2crm MySQL/MariaDB database.

Setup:
    pip install mysql-connector-python python-dotenv

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
import mysql.connector
from mysql.connector import Error

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "connection_timeout": 5,
}

def execute_query(query, as_dict=True):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=as_dict)
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print("Query execution failed:", e)
        return None
    finally:
        if "conn" in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def get_interesting_produktionslinien():
    query = f"""SELECT
    p.*,
    (
        SELECT k.Firma
        FROM kunden k
        WHERE k.KU_NR = p.ku_nr
          AND k.Firma <> ''
        ORDER BY k.zeitpunkt DESC
        LIMIT 1
    ) AS firma,
    (
        SELECT k.Firma2
        FROM kunden k
        WHERE k.KU_NR = p.ku_nr
          AND k.Firma <> ''
        ORDER BY k.zeitpunkt DESC
        LIMIT 1
    ) AS firma2,
    (
        SELECT k.Ort
        FROM kunden k
        WHERE k.KU_NR = p.ku_nr
          AND k.Firma <> ''
        ORDER BY k.zeitpunkt DESC
        LIMIT 1
    ) AS ort
FROM produktionslinie p
WHERE p.vp_delete = 0
  AND p.vo_status IN (2)                                                   -- offene Vorgänge
  AND p.vo_nummer NOT LIKE 'AN%'                         -- keine Angebote
  AND p.produktionslinie LIKE 'Fahrgestelle%'
  AND p.id IN (
      SELECT MAX(p2.id)
      FROM produktionslinie p2
      WHERE p2.vo_nummer NOT LIKE 'AN%'
      GROUP BY p2.vp_id, p2.vo_id
  )
ORDER BY p.vp_lieferdatum ASC, p.vo_nummer ASC;
"""
    result = execute_query(query, as_dict=True)
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
            "kundenname": row.get("firma", None) or row.get("firma2", None) or row.get("ort", None),
            "vorgangsnummer": row.get("vo_nummer", None),
            "vorgangstext": row.get("vorgang_text", None),
            "artikelbeschreibung": row.get("beschreibung_kurz", None),
            "artikelnr": row.get("ar_nr", None)
        }
        sanitized.append(sanitized_row)
    return sanitized

if __name__ == "__main__":
    print("Fetching interesting produktionslinien...")
    produktionslinien = get_interesting_produktionslinien()
    print(f"Fetched {len(produktionslinien)} rows.")