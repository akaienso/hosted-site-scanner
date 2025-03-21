# Copyright (c) 2025 Rob Moore <io@rmoore.dev>
# db.py
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()  # Loads variables from .env if present

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', '')
    )
    
def get_websites():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, base_url FROM websites")
    websites = cursor.fetchall()
    conn.close()
    return websites

def store_form_result(website_id, page_url, form_count, captchas):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO form_scan_results (website_id, page_url, form_count, captchas_found)
        VALUES (%s, %s, %s, %s)
    """, (website_id, page_url, form_count, ','.join(captchas)))
    conn.commit()
    conn.close()