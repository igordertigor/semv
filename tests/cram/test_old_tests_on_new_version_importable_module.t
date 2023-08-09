This test checks one of the main ideas of Stephan Bönnemann's talk: If the previous version's tests fail when running against a new version, then that version is likely a major version.

  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in /tmp/cramtests-*/test_old_tests_on_new_version_importable_module.t/.git/ (glob)
  [master (root-commit) *] docs(readme): Add readme (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 README.md

Create some setup:
Tox
  $ echo "[tox]" > tox.ini
  $ echo "isolated_build = true" >> tox.ini
  $ echo "envlist = unit" >> tox.ini
  $ echo "" >> tox.ini
  $ echo "[testenv:unit]" >> tox.ini
  $ echo "deps = pytest" >> tox.ini
  $ echo "commands = pytest {posargs} tests.py" >> tox.ini
  $ echo "" >> tox.ini
  $ echo "[testenv:build]" >> tox.ini
  $ echo "deps = build" >> tox.ini
  $ echo "skip_install = true" >> tox.ini
  $ echo "skip_dist = true" >> tox.ini
  $ echo "commands = python -m build" >> tox.ini

pyproject
  $ echo "[project]" > pyproject.toml
  $ echo 'name = "mypack"' >> pyproject.toml
  $ echo 'dynamic = ["version"]' >> pyproject.toml
  $ echo "" >> pyproject.toml
  $ echo "[build-system]" >> pyproject.toml
  $ echo 'requires = ["setuptools>=45", "setuptools_scm[toml]>=6.2"]' >> pyproject.toml
  $ echo 'build-backend = "setuptools.build_meta"' >> pyproject.toml
  $ echo "" >> pyproject.toml
  $ echo "[tool.setuptools_scm]" >> pyproject.toml

source
  $ echo "def f(x, y):" > mypack.py
  $ echo "    return x + y" >> mypack.py

tests
  $ echo "import mypack" > tests.py
  $ echo "" >> tests.py
  $ echo "def test_regular_sum():" >> tests.py
  $ echo "    assert mypack.f(2, 1) == 3" >> tests.py

Commit
  $ git add mypack.py tests.py tox.ini pyproject.toml
  $ git commit -m "feat(mypack): Initial implementation"
  [master *] feat(mypack): Initial implementation (glob)
   4 files changed, 28 insertions(+)
   create mode 100644 mypack.py
   create mode 100644 pyproject.toml
   create mode 100644 tests.py
   create mode 100644 tox.ini
  $ git tag v1.0.0

Now configure the checks
  $ echo "" >> pyproject.toml
  $ echo "[tool.semv.checks]" >> pyproject.toml
  $ echo 'RunPreviousVersionsTestsTox = {testenv = "unit"}' >> pyproject.toml
  $ git add pyproject.toml
  $ git commit -m "chore(semv): Add semv config"
  [master *] chore(semv): Add semv config (glob)
   1 file changed, 3 insertions(+)

Introduce a breaking change
  $ echo "def f(x, y):" > mypack.py
  $ echo "    return x * y" >> mypack.py
  $ git add mypack.py
  $ git commit -m 'feat(mypack): Multiplications are cooler'
  [master *] feat(mypack): Multiplications are cooler (glob)
   1 file changed, 1 insertion(+), 1 deletion(-)
  $ semv
  _______________________________ test_regular_sum _______________________________
  
      def test_regular_sum():
  *       assert mypack.f(2, 1) == 3 (glob)
  E       assert 2 == 3
  E        +  where 2 = <function f at *>(2, 1) (glob)
  E        +    where <function f at *> = mypack.f (glob)
  
  tests.py:4: AssertionError
  =========================== short test summary info ============================
  FAILED tests.py::test_regular_sum - assert 2 == 3
  ===========================    end of test report   ============================
  ERROR: Commits suggest minor increment, but checks imply major increment
  [3]
