# Hosted Site Scanner

Hosted Site Scanner is a modular Python tool for scanning hosted websites to detect forms, CAPTCHA protection, and other site-level features. Designed for WordPress site hosts and web service providers, this tool helps identify potential spam vectors, enforce security standards, and automate site audits.

## Features

- 🔎 Automatically crawls websites for pages containing HTML forms
- 🛡 Detects CAPTCHA implementations:
  - Google reCAPTCHA (v2/v3)
  - Cloudflare Turnstile
  - hCaptcha
- 📂 Logs findings to a MySQL database for auditing and reporting
- 🔧 Modular design for future scanners (e.g., plugin audits, SEO checks, etc.)
- 🔸 Configurable crawler depth and timeout settings
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

Create a `.env` file in the root of the project with the following contents:

```env
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_NAME=your_db_name

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

## Contributing

Contributions are welcome! Please open an issue or create a pull request with your proposed changes. For larger changes, please start with a discussion.

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

**Rob Moore**  
📧 [io@rmoore.dev](mailto:io@rmoore.dev)  
🌐 [rmoore.dev](https://rmoore.dev)


