  $ bash "$TESTDIR"/setup.sh
  $ echo "print('Hello')" > myscript.py
  $ git add myscript.py
  $ git commit -m 'feat(myscript): Print a message'
  $ git tag $(semv)
  $ git tag
  $ echo "print('Hello world!')" > myscript.py
  $ git add myscript.py
  $ git commit -m 'feat(myscript): Improved message'
  $ echo "def greet() -> str:" > myscript.py
  $ echo "    print('Hello world!')" >> myscript.py
  $ echo "" >> myscript.py
  $ echo "if __name__ == '__main__'" >> myscript.py
  $ echo "    geet()" >> myscript.py
  $ git add myscript.py
  $ git commit -m 'feat: Convert to api'
  $ cat myscript.py | sed s/geet/greet/  > dummy
  $ mv dummy myscript.py
  $ git add myscript.py
  $ git commit -m 'fix(myscript): fix typo'
  $ semv --changelog
  # New features
  - General: Convert to api
  - myscript: Improved message

  # Fixes
  - myscript: fix typo
