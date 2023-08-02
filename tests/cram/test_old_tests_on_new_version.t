This test checks one of the main ideas of Stephan Bönnemann's talk: If the previous version's tests fail when running against a new version, then that version is likely a major version.

  $ bash "$TESTDIR"/setup.sh

Create some setup:
Tox
  $ echo "[tox]" > tox.ini
  $ echo "envlist = unit" >> tox.ini
  $ echo "" >> tox.ini
  $ echo "[testenv:unit]" >> tox.ini
  $ echo "deps = pytest" >> tox.ini
  $ echo "commands = pytest tests.py" >> tox.ini

pyproject
  $ echo "[project]" > pyproject.toml
  $ echo 'name = "mypack"' >> pyproject.toml
  $ echo 'dynamic = ["version"]' >> pyproject.toml
  $ echo "" >> pyproject.toml
  $ echo "[build-system]" >> pyproject.toml
  $ echo 'requires = ["setuptools>=45", "setuptools_scm[toml]>=6.2"]' >> pyproject.toml
  $ echo 'build-backend = "setuptools.build_meta"' >> pyproject.toml

source
  $ echo "def f(x, y):" > mypack.py
  $ echo "    return x + y" >> mypack.py

tests
  $ echo "import mypack" > tests.py
  $ echo "" >> tests.py
  $ echo "def test_regular_sum():" >> tests.py
  $ echo "    assert mypack.f(2, 1) == 3" >> tests.py

make sure this works
  $ tox

Commit
  $ git add mypack.py tests.py tox.ini pyproject.toml
  $ git commit -m "feat(mypack): Initial implementation"
  $ git tag v1.0.0

Now configure the checks
  $ echo "" >> pyproject.toml
  $ echo "[tool.semv]" >> pyproject.toml
  $ echo 'checks = ["run_previous_version_tests"]' >> pyproject.toml
  $ git add pyproject.toml
  $ git commit -m "chore(semv): Add semv config"

Introduce a breaking change
  $ echo "def f(x, y):" > mypack.py
  $ echo "    return x * y" >> mypack.py
  $ git add mypack.py
  $ git commit -m 'feat(mypack): Multiplications are cooler'
  $ semv
