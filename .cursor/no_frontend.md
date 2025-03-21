---
description: No Frontend Stack
globs: "*"
---

# No Frontend Stack

<rule>
name: no_frontend
description: Disallow frontend libraries and tools in this backend-only repo
filters:
  - type: content
    pattern: "(?i)\b(webpack|vite|react|angular|vue|tailwind|eslint|babel)\b"
  - type: file_extension
    pattern: "\.(js|jsx|ts|tsx|html|css|scss)$"
  - type: file_name
    pattern: "^package\.json$"
actions:
  - type: reject
    message: |
      This project is strictly Python-based. Frontend tooling and JS frameworks are not permitted.
  - type: suggest
    message: |
      If you need UI or API docs, use Python-based tools like Flask or MkDocs.
</rule>