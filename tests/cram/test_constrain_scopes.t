  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in */.git/ (glob)
  [master (root-commit) *] docs(readme): Add readme (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 README.md
  $ echo '[tool.semv]' > pyproject.toml
  $ echo 'invalid_commit_action = "error"' >> pyproject.toml
  $ echo 'valid_scopes = ["myscript", "logic"]' >> pyproject.toml
  $ echo "print('Hello')" > myscript.py
  $ git add myscript.py
  $ git commit -m 'feat(myscript): Print a message'
  [master *] feat(myscript): Print a message (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 myscript.py
  $ git tag $(semv)
  $ git tag
  v0.0.0
  v0.1.0
  $ echo "print('Hello world!')" > myscript.py
  $ git add myscript.py
  $ git commit -m 'feat(myscipt): Improved message'
  [master *] feat(myscipt): Improved message (glob)
   1 file changed, 1 insertion(+), 1 deletion(-)
  $ echo "def greet() -> str:" > myscript.py
  $ echo "    print('Hello world!')" >> myscript.py
  $ echo "" >> myscript.py
  $ echo "if __name__ == '__main__'" >> myscript.py
  $ echo "    geet()" >> myscript.py
  $ git add myscript.py
  $ git commit -m 'feat: Convert to api'
  [master *] feat: Convert to api (glob)
   1 file changed, 5 insertions(+), 1 deletion(-)
  $ semv
  ERROR: Invalid commit scope: * feat(myscipt): Improved message (glob)
  [2]
