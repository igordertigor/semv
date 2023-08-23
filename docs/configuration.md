# Configuration

This page lists all possible configuration options along with their defaults.

- `tool.semv.invalid_commit_action = "warning"`: Action to take if encountering an invalid commit&mdash;typically a commit for which the commit message doesn't have the correct form

 Here are the
defaults:
```toml
[tool.semv]
invalid_commit_action = "warning"  # Could also be "error" or "skip"

[tool.semv.types]
feat = "minor"
fix = "patch"
perf = "patch"
chore = "valid"
test = "valid"
docs = "valid"
ci = "valid"
refactor = "valid"
style = "valid"
```
