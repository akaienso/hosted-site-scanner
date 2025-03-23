# crawler.py
#
# Copyright (c) 2025 Rob Moore

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

headers = {'User-Agent': config['crawler']['user_agent']}
timeout = int(config['crawler']['timeout'])

# Map captcha names to known markers, for naive detection:
captcha_indicators = {
    'reCAPTCHA': ['google.com/recaptcha', 'g-recaptcha', 'grecaptcha'],
    'Turnstile': ['cf-turnstile', 'challenges.cloudflare.com/turnstile'],
    'hCaptcha': ['hcaptcha.com/1/api.js', 'h-captcha']
}

# Map form plugin names to known markers, for naive detection:
form_plugin_signatures = {
    'Contact Form 7': ['wpcf7-form', 'contact-form-7'],
    'Gravity Forms': ['gform_wrapper', 'gravityforms'],
    'WPForms': ['wpforms-form', 'wpforms-container'],
    'Formidable Forms': ['frm_forms', 'formidable'],
    'Ninja Forms': ['nf-form', 'ninja-forms'],
    'Elementor': ['elementor-form', 'elementor-form-fields'],
}

def detect_form_plugin(html):
    lower_html = html.lower()
    for name, markers in form_plugin_signatures.items():
        if any(marker in lower_html for marker in markers):
            return name
    return 'Unknown'

def detect_wp_version(html):
    """
    Attempt to parse out WordPress version from meta tags (naive example).
      e.g. <meta name="generator" content="WordPress 6.1.1" />
    """
    match = re.search(r'<meta name="generator" content="WordPress\s*([\d.]+)"', html, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def detect_theme(html):
    """
    Detect active theme name by searching for '/wp-content/themes/THEME_NAME/' in the HTML.
    Very naive approach—some sites rename or hide 'wp-content'.
    """
    match = re.search(r'/wp-content/themes/([^/]+)/', html)
    if match:
        return match.group(1)
    return None

def detect_admin_email(html):
    """
    Attempt to detect a mailto link. 
    Many WordPress sites won't publicly show the admin email, but let's try anyway.
    """
    match = re.search(r'mailto:([^"]+)', html, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def detect_forms_and_captcha(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    forms = soup.find_all('form')
    if not forms:
        return None

    captchas_found = set()
    lower_html = html.lower()

    for tag in soup.find_all(['script', 'iframe'], src=True):
        src = tag['src'].lower()
        for name, indicators in captcha_indicators.items():
            if any(indicator in src for indicator in indicators):
                captchas_found.add(name)

    for name, indicators in captcha_indicators.items():
        if any(indicator in lower_html for indicator in indicators):
            captchas_found.add(name)

    plugin = detect_form_plugin(html)

    return {
        'url': url,
        'form_count': len(forms),
        'captchas': list(captchas_found) or ['None'],
        'plugin': plugin
    }

def is_internal(url, root_domain):
    """
    Check if a given URL is within the same registered domain.
    Using tldextract to get the domain portion and compare.
    """
    return tldextract.extract(url).registered_domain == root_domain

def crawl(base_url, max_pages=30):
    """
    Approach B:
    1. Fetch the base_url (homepage) once, to detect WP version, theme, admin_email, etc.
    2. Then do the multi-page crawl for forms/captchas.

    Returns:
        site_info (dict) : { 'wp_version': ..., 'theme': ..., 'admin_email': ... }
        results   (list) : each item is { 'url': ..., 'form_count': ..., 'captchas': [...] }
    """
    site_info = {
        'wp_version': None,
        'theme': None,
        'admin_email': None
    }

    # Step 1: Fetch homepage to gather site-level info
    try:
        r_home = requests.get(base_url, headers=headers, timeout=timeout)
        if r_home.ok:
            html_home = r_home.text
            site_info['wp_version'] = detect_wp_version(html_home)
            site_info['theme']      = detect_theme(html_home)
            site_info['admin_email'] = detect_admin_email(html_home)
    except:
        pass  # if we can't fetch homepage for some reason, just move on

    # Step 2: Multi-page form scan
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

            # Detect forms/captchas on this page
            result = detect_forms_and_captcha(r.text, url)
            if result:
                results.append(result)

            # Discover more links to crawl
            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if is_internal(next_url, root_domain) and next_url not in visited:
                    to_visit.append(next_url)

        except:
            continue

    return site_info, results
