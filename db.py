import mysql.connector
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

db_config = config['database']

def get_connection():
    return mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
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