---
description: Auto-commit Python changes with Conventional Commits
globs: "*.py"
---

# Conventional Commits for Python

<rule>
name: commit_python_conventionally
description: Automatically commit Python changes with conventional commit message
filters:
  - type: event
    pattern: "file_change"
  - type: file_extension
    pattern: ".py"
actions:
  - type: execute
    command: |
      git add "$FILE"
      git commit -m "feat(${FILE%%/*}): update $FILE"
</rule>