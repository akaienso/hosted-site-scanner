# Hosted Site Scanner

Hosted Site Scanner is a modular Python tool for scanning hosted websites to detect forms, CAPTCHA protection, and other site-level features. Designed for WordPress site hosts and web service providers, this tool helps identify potential spam vectors, enforce security standards, and automate site audits.

## Features

- 🔎 Automatically crawls websites for pages containing HTML forms
- 🛡 Detects CAPTCHA implementations:
  - Google reCAPTCHA (v2/v3)
  - Cloudflare Turnstile
  - hCaptcha
- 🗂 Logs findings to a MySQL database for auditing and reporting
- 🔧 Modular design for future scanners (e.g., plugin audits, SEO checks, etc.)
- 🕸 Configurable crawler depth and timeout settings
- ✅ Lightweight and easy to deploy

## Getting Started

### Requirements

- Python 3.8+
- MySQL or MariaDB
- pip (Python package manager)

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/hosted-site-scanner.git
cd hosted-site-scanner
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

### Configuration

This project reads its database credentials from environment variables. For local development, you can store them in a `.env` file in the project root (ignored by Git).

Example `.env` file:

```bash
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_secure_password
DB_NAME=hosted_site_scanner

MAX_PAGES=30
TIMEOUT=10
USER_AGENT=Mozilla/5.0 (compatible; HostedSiteScanner/1.0)
```

> **Note**: The `.env` file is ignored via `.gitignore` and should never be committed.

### Database Setup

Run the following SQL to create necessary tables:

```sql
CREATE TABLE websites (
  id INT AUTO_INCREMENT PRIMARY KEY,
  base_url VARCHAR(255) NOT NULL,
  last_scanned DATETIME NULL
);

CREATE TABLE form_scan_results (
  id INT AUTO_INCREMENT PRIMARY KEY,
  website_id INT NOT NULL,
  page_url TEXT NOT NULL,
  form_count INT NOT NULL,
  captchas_found VARCHAR(255),
  scan_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (website_id) REFERENCES websites(id) ON DELETE CASCADE
);
```

### Usage

Run the scanner:

```bash
python main.py
```

The tool will:

1. Read target sites from the `websites` table.
2. Crawl up to `MAX_PAGES` per site.
3. Log form pages and CAPTCHA presence to `form_scan_results`.

---

## GitHub Actions (Optional CI)

To enable automatic linting and syntax checks on each push or pull request, create the following workflow file:

**Path:** `.github/workflows/python-lint.yml`

```yaml
name: Python Lint & Syntax Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run compile check
        run: |
          python -m compileall .

      - name: Check formatting with black
        run: |
          pip install black
          black --check .

      - name: Run flake8 linting
        run: |
          pip install flake8
          flake8 .
```

This workflow checks for Python syntax errors, enforces code formatting using `black`, and runs `flake8` for PEP8 compliance.

---

## Contributing

Contributions are welcome! Please open an issue or create a pull request with your proposed changes. For larger changes, please start with a discussion.

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

**Rob Moore**  
📧 [io@rmoore.dev](mailto:io@rmoore.dev)  
🌐 [rmoore.dev](https://rmoore.dev)

---

## .gitignore

```gitignore
__pycache__/
.env
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
.env.*
.idea/
.vscode/
.DS_Store
*.log
*.zip
```

## LICENSE (MIT)

```
MIT License

Copyright (c) 2025 Rob Moore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

