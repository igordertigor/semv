  $ semv --list-types
  Implies minor increment:
    feat
  Implies patch increment:
    fix, perf
  Other valid types:
    chore, ci, docs, refactor, style, test

  $ echo "[tool.semv.types]" > pyproject.toml
  $ echo 'break = "major"' >> pyproject.toml
  $ echo 'feat = "minor"' >> pyproject.toml
  $ echo 'perf = "minor"' >> pyproject.toml
  $ echo 'fix = "patch"' >> pyproject.toml
  $ echo 'chore = "valid"' >> pyproject.toml
  $ echo 'docs = "valid"' >> pyproject.toml
  $ semv --list-types
  Implies major increment:
    break
  Implies minor increment:
    feat, perf
  Implies patch increment:
    fix
  Other valid types:
    chore, docs
