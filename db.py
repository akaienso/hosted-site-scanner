# db.py
#
# Copyright (c) 2025 Rob Moore

import mysql.connector
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

db_config = config['database']

def get_connection():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

def get_websites():
    """
    Fetch all websites from the 'websites' table.
    Expects columns: id, base_url, plus any new columns you've added.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, base_url FROM websites")
    websites = cursor.fetchall()
    conn.close()
    return websites

def update_website_metadata(website_id, wp_version, theme, admin_email):
    """
    Update the site-level info in the 'websites' table.
    If you also want to store a 'last_scanned' timestamp, do that here as well.
    """
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE websites
           SET wp_version = %s,
               active_theme = %s,
               admin_email = %s,
               last_scanned = NOW()
         WHERE id = %s
    """
    cursor.execute(sql, (wp_version, theme, admin_email, website_id))
    conn.commit()
    conn.close()

def store_form_result(website_id, page_url, form_count, captchas, plugin_installed):
    conn = get_connection()
    cursor = conn.cursor()

    captchas_str = ",".join(captchas) if captchas else None

    sql = """
        INSERT INTO website_forms
          (website_id, page_url, form_count, captchas_found, plugin_installed)
        VALUES
          (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (website_id, page_url, form_count, captchas_str, plugin_installed))
    conn.commit()
    conn.close()

