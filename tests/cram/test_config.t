  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in */.git/ (glob)
  [master (root-commit) *] docs(readme): Add readme (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 README.md

  $ echo "print('Hello')" > myscript.py
  $ git add myscript.py
  $ git commit -m 'Print a message'
  [master *] Print a message (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 myscript.py

  $ echo "print('Hello world')" > myscript.py
  $ git add myscript.py
  $ git commit -m 'fix(myscript): Meant to greet world'
  [master *] fix(myscript): Meant to greet world (glob)
   1 file changed, 1 insertion(+), 1 deletion(-)

  $ echo "[tool.semv]" > pyproject.toml
  $ echo 'invalid_commit_action = "warning"' >> pyproject.toml
  $ semv
  WARNING: Invalid commit: * Print a message (glob)
  v0.0.1 (no-eol)

  $ echo "[tool.semv]" > pyproject.toml
  $ echo 'invalid_commit_action = "skip"' >> pyproject.toml
  $ semv
  v0.0.1 (no-eol)

  $ echo "[tool.semv]" > pyproject.toml
  $ echo 'invalid_commit_action = "error"' >> pyproject.toml
  $ semv
  ERROR: Invalid commit: * Print a message (glob)
  [2]
