from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests, time
import tldextract
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

captcha_indicators = {
    'reCAPTCHA': ['google.com/recaptcha', 'g-recaptcha', 'grecaptcha'],
    'Turnstile': ['cf-turnstile', 'challenges.cloudflare.com/turnstile'],
    'hCaptcha': ['hcaptcha.com/1/api.js', 'h-captcha']
}

headers = {'User-Agent': config['crawler']['user_agent']}
timeout = int(config['crawler']['timeout'])

def is_internal(url, root_domain):
    return tldextract.extract(url).registered_domain == root_domain

def detect_forms_and_captcha(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    forms = soup.find_all('form')
    if not forms:
        return None
    lower_html = html.lower()
    found = [name for name, markers in captcha_indicators.items() if any(m in lower_html for m in markers)]
    return {'url': url, 'form_count': len(forms), 'captchas': found or ['None']}

def crawl(base_url, max_pages=30):
    visited = set()
    to_visit = [base_url]
    root_domain = tldextract.extract(base_url).registered_domain
    results = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            if not r.ok:
                continue
            result = detect_forms_and_captcha(r.text, url)
            if result:
                results.append(result)

            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if is_internal(next_url, root_domain) and next_url not in visited:
                    to_visit.append(next_url)
        except:
            continue
    return results