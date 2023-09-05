  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in */.git/ (glob)
  [master (root-commit) *] docs(readme): Add readme (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 README.md
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
  $ git commit -m 'feat(myscript): Improved message'
  [master *] feat(myscript): Improved message (glob)
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
  $ cat myscript.py | sed s/geet/greet/  > dummy
  $ mv dummy myscript.py
  $ git add myscript.py
  $ git commit -m 'fix(myscript): fix typo'
  [master *] fix(myscript): fix typo (glob)
   1 file changed, 1 insertion(+), 1 deletion(-)
  $ semv --changelog
  # New features
  - General: Convert to api
  - myscript: Improved message
  
  # Fixes
  - myscript: fix typo

Add breaking change
  $ echo "def greet(name) -> str:" > myscript.py
  $ echo "    print(f'Hello {name}!')" >> myscript.py
  $ echo "" >> myscript.py
  $ echo "if __name__ == '__main__':" >> myscript.py
  $ echo "    greet('world')" >> myscript.py
  $ git add myscript.py
  $ echo 'feat(myscript): Need name' > msg
  $ echo '' >> msg
  $ echo 'BREAKING CHANGE: Need to pass a name to greet now' >> msg
  $ git commit -F msg
  [master *] feat(myscript): Need name (glob)
   1 file changed, 4 insertions(+), 4 deletions(-)
  $ semv --changelog
  # Breaking changes
  - myscript: Need name
    - Need to pass a name to greet now
  
  # New features
  - General: Convert to api
  - myscript: Improved message
  
  # Fixes
  - myscript: fix typo
  $ echo "def greet(name) -> str:" > myscript.py
  $ echo "    'Print greeting message'" >> myscript.py
  $ echo "    print(f'Hello {name}!')" >> myscript.py
  $ echo "" >> myscript.py
  $ echo "if __name__ == '__main__':" >> myscript.py
  $ echo "    greet('world')" >> myscript.py
  $ git add myscript.py
  $ git commit -m 'feat(myscript): Add docstring'
  [master *] feat(myscript): Add docstring (glob)
   1 file changed, 1 insertion(+)
  $ semv --changelog
  # Breaking changes
  - myscript: Need name
    - Need to pass a name to greet now
  
  # New features
  - General: Convert to api
  - myscript:
    - Improved message
    - Add docstring
  
  # Fixes
  - myscript: fix typo

  $ semv --changelog=json
  {
    "breaking_changes": [
      {
        "scope": "myscript",
        "message": "Need name",
        "info": [
          "Need to pass a name to greet now"
        ]
      }
    ],
    "major_changes": {},
    "minor_changes": {
      "feat": [
        {
          "scope": "general",
          "messages": [
            "Convert to api"
          ]
        },
        {
          "scope": "myscript",
          "messages": [
            "Improved message",
            "Add docstring"
          ]
        }
      ]
    },
    "patch_changes": {
      "fix": [
        {
          "scope": "myscript",
          "messages": [
            "fix typo"
          ]
        }
      ]
    }
  }
