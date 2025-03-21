---
description: Enforce Python code quality via formatting and linting
globs: "*.py"
---

# Python Quality

<rule>
name: python_quality_enforcement
description: Ensure Python code is properly formatted and passes lint checks
filters:
  - type: event
    pattern: "file_save"
actions:
  - type: execute
    command: |
      black "$FILE" && flake8 "$FILE"
</rule>