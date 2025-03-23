# main.py
#
# Copyright (c) 2025 Rob Moore

from configparser import ConfigParser
import requests
from db import get_websites, update_website_metadata, store_form_result
from crawler import crawl

config = ConfigParser()
config.read('config.ini')
max_pages = int(config['crawler']['max_pages'])

def main():
    # 1. Load websites from DB (which have id, base_url, etc.)
    websites = get_websites()

    # 2. For each website, run crawl(...) to get site-level info and form data
    for site in websites:
        site_id = site['id']
        base_url = site['base_url']

        print(f"\nScanning: {base_url}")

        # Approach B: crawler.crawl() returns (site_info, form_results)
        site_info, form_results = crawl(base_url, max_pages=max_pages)

        # 3. Update the site-level metadata (e.g., WP version, theme, admin email)
        wp_version  = site_info['wp_version']
        theme       = site_info['theme']
        admin_email = site_info['admin_email']

        update_website_metadata(site_id, wp_version, theme, admin_email)

        # 4. Insert the form scan results into your per-page table
        for result in form_results:
            store_form_result(
                website_id=site_id,
                page_url=result['url'],
                form_count=result['form_count'],
                captchas=result['captchas'],
                plugin_installed=result['plugin']
            )

if __name__ == '__main__':
    main()