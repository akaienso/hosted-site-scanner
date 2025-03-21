---
description: Auto-commit changes with conventional commit messages
globs: "*.py"
---

# Auto Commit on Change

<rule>
name: auto_commit_conventional
description: Automatically commit file changes with structured commit messages
filters:
  - type: event
    pattern: "file_change"
  - type: file_extension
    pattern: ".py"
actions:
  - type: execute
    command: |
      git add "$FILE"
      git commit -m "chore(${FILE%%/*}): update $FILE"
</rule>