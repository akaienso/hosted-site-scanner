# bulk_add_websites.py

import mysql.connector
from db import get_connection

def bulk_insert_websites(urls):
    conn = get_connection()
    cursor = conn.cursor()
    # Build a list of tuples like [(url1,), (url2,), ...]
    data = [(url,) for url in urls]
    sql = "INSERT INTO websites (base_url) VALUES (%s)"
    cursor.executemany(sql, data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Suppose you have a text file 'sites.txt' with one URL per line
    with open("sites.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]  # skip blank lines

    bulk_insert_websites(lines)
    print(f"Inserted {len(lines)} websites.")

