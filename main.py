from db import get_websites, store_form_result
from crawler import crawl
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

max_pages = int(config['crawler']['max_pages'])

def main():
    websites = get_websites()
    for site in websites:
        print(f"Scanning: {site['base_url']}")
        results = crawl(site['base_url'], max_pages=max_pages)
        for result in results:
            print(f"  - Found form at {result['url']} with CAPTCHA: {result['captchas']}")
            store_form_result(site['id'], result['url'], result['form_count'], result['captchas'])

if __name__ == '__main__':
    main()