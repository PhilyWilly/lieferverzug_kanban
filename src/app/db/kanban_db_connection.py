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
    now = datetime.now()
    current_year = now.year
    current_week = now.isocalendar()[1]
    print(f"Current year: {current_year}, Current week: {current_week}")
    # query = f"""
    # SELECT 
    #     vp_liefer_kwj as jahr, 
    #     vp_liefer_kw as kw ,
    #     ku_anschrift as kundenname,
    #     vo_nummer as vorgangsnummer,
    #     vorgang_text as vorgangstext,
    #     beschreibung_kurz as artikelbeschreibung,
    #     ar_nr as artikelnr
    # FROM produktionslinie 
    # WHERE 
    #     vo_status IN (2)
    #     AND vp_delete = 0
    # ORDER BY vp_liefer_kwj, vp_liefer_kw
    # LIMIT 10;
    # """
    query = f"""
        SELECT 
            vp_liefer_kwj as jahr, 
            vp_liefer_kw as kw,
            ku_anschrift as kundenname,
            vo_nummer as vorgangsnummer,
            vorgang_text as vorgangstext,
            beschreibung_kurz as artikelbeschreibung,
            ar_nr as artikelnr
        FROM produktionslinie
        WHERE 
            vo_nummer NOT LIKE 'AN%'
            AND vp_delete = 0
            AND vo_status IN (2)
            AND id IN (
                SELECT MAX(id)
                FROM (
                    SELECT id, vo_id, vp_id
                    FROM produktionslinie
                    WHERE vo_nummer NOT LIKE 'AN%'
                ) AS tmp
                GROUP BY vp_id, vo_id
            )
        ORDER BY vp_liefer_kwj, vp_liefer_kw;"""
    result = execute_query(query, as_dict=True)
    if not result:
        return None
    return result

def testy():
    query = f"""
    SELECT 
        *
    FROM produktionslinie
    WHERE 
        vo_nummer NOT LIKE 'AN%'
        AND vp_delete = 0
        AND vo_nummer LIKE '%204550%'
        AND vo_status IN (2)
        AND id IN (
            SELECT MAX(id)
            FROM (
                SELECT id, vo_id, vp_id
                FROM produktionslinie
                WHERE vo_nummer NOT LIKE 'AN%'
            ) AS tmp
            GROUP BY vp_id, vo_id
        )
    ORDER BY vp_liefer_kwj, vp_liefer_kw LIMIT 50;"""
    result = execute_query(query, as_dict=True)
    for row in result:
        print("------------------------------------------")
        for key, value in row.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    testy()