# Copyright (c) 2025 Rob Moore <io@rmoore.dev>

import sys
from datetime import datetime

if len(sys.argv) != 2:
    print("Usage: python add_license.py <filename>")
    sys.exit(1)

year = datetime.now().year
filename = sys.argv[1]

try:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    license_header = f"# Copyright (c) {year} Rob Moore <io@rmoore.dev>\n"

    if content.startswith(license_header):
        print("License already present.")
        sys.exit(0)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(license_header + content)

    print(f"License header added to {filename}")
except Exception as e:
    print(f"Failed to update {filename}: {e}")
    sys.exit(1)