---
description: Prevent frontend-related tooling in this Python project
globs: "*"
---

# Clamp Frontend Tech

<rule>
name: disallow_frontend
description: Prevent use of JS-based frontend tooling or frameworks in a backend project
filters:
  - type: content
    pattern: "(?i)\b(react|vue|angular|svelte|tailwind|vite|webpack|babel)\b"
  - type: file_extension
    pattern: "\.(js|jsx|ts|tsx|html|css|scss)$"
  - type: file_name
    pattern: "^package\.json$"
actions:
  - type: reject
    message: |
      Hosted Site Scanner is strictly Python-based. Please do not introduce frontend tooling or JavaScript frameworks.
</rule>