---
description: Enforce license headers in Python files
globs: "*.py"
---

# License Headers

<rule>
name: license_header_dynamic
description: Adds Rob Moore license with current year to Python files
filters:
  - type: file_extension
    pattern: ".py"
  - type: event
    pattern: "file_create"
actions:
  - type: execute
    command: |
      python scripts/add_license.py "$FILE"
</rule>