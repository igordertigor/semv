This test checks one of the main ideas of Stephan Bönnemann's talk: If the previous version's tests fail when running against a new version, then that version is likely a major version.

  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in /tmp/cramtests-*/test_old_tests_on_new_version.t/.git/ (glob)
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
  $ mkdir src
  $ echo "def f(x, y):" > src/mypack.py
  $ echo "    return x + y" >> src/mypack.py

tests
  $ echo "import mypack" > tests.py
  $ echo "" >> tests.py
  $ echo "def test_regular_sum():" >> tests.py
  $ echo "    assert mypack.f(2, 1) == 3" >> tests.py

make sure this works
  $ tox
  unit: install_deps> python -I -m pip install pytest
  .pkg: install_requires> python -I -m pip install 'setuptools>=45' 'setuptools_scm[toml]>=6.2'
  .pkg: _optional_hooks> python */semv/.venv/lib/python3.*/site-packages/pyproject_api/_backend.py True setuptools.build_meta (glob)
  .pkg: get_requires_for_build_sdist> python */semv/.venv/lib/python3.*/site-packages/pyproject_api/_backend.py True setuptools.build_meta (glob)
  .pkg: build_sdist> python */semv/.venv/lib/python3.*/site-packages/pyproject_api/_backend.py True setuptools.build_meta (glob)
  unit: install_package> python -I -m pip install --force-reinstall --no-deps /tmp/cramtests-*/test_old_tests_on_new_version.t/.tox/.tmp/package/1/mypack-0.0.0.tar.gz (glob)
  unit: commands[0]> pytest tests.py
  ============================= test session starts ==============================
  platform linux -- Python 3.*, pytest-7.4.0, pluggy-1.2.0
  cachedir: .tox/unit/.pytest_cache
  rootdir: /tmp/cramtests-*/test_old_tests_on_new_version.t (glob)
  collected 1 item
  
  tests.py .                                                               [100%]
  
  ============================== 1 passed in 0.00s ===============================
  .pkg: _exit> python */semv/.venv/lib/python3.*/site-packages/pyproject_api/_backend.py True setuptools.build_meta (glob)
    unit: OK (*=setup[*]+cmd[*] seconds) (glob)
    congratulations :) (* seconds) (glob)

Commit
  $ git add src/mypack.py tests.py tox.ini pyproject.toml
  $ git commit -m "feat(mypack): Initial implementation"
  [master *] feat(mypack): Initial implementation (glob)
   4 files changed, 28 insertions(+)
   create mode 100644 pyproject.toml
   create mode 100644 src/mypack.py
   create mode 100644 tests.py
   create mode 100644 tox.ini
  $ git tag v1.0.0

Now configure the checks
  $ echo "" >> pyproject.toml
  $ echo "[tool.semv.checks]" >> pyproject.toml
  $ echo 'RunPreviousVersionsTestsTox = {toxenv = "unit"}' >> pyproject.toml
  $ git add pyproject.toml
  $ git commit -m "chore(semv): Add semv config"
  [master *] chore(semv): Add semv config (glob)
   1 file changed, 3 insertions(+)

Introduce a breaking change
  $ echo "def f(x, y):" > src/mypack.py
  $ echo "    return x * y" >> src/mypack.py
  $ git add src/mypack.py
  $ git commit -m 'feat(mypack): Multiplications are cooler'
  [master *] feat(mypack): Multiplications are cooler (glob)
   1 file changed, 1 insertion(+), 1 deletion(-)
  $ semv
  unit: install_deps> python -I -m pip install pytest
  unit: install_package> python -I -m pip install --force-reinstall --no-deps /tmp/cramtests-*/test_old_tests_on_new_version.t/dist/mypack-1.0.1.dev2+*-py3-none-any.whl (glob)
  unit: commands[0]> pytest -v tests.py
  ============================= test session starts ==============================
  platform linux -- Python 3.*, pytest-7.4.0, pluggy-1.2.0 -- /tmp/cramtests-*/.tox/unit/bin/python (glob)
  cachedir: .tox/unit/.pytest_cache
  rootdir: /tmp/cramtests-* (glob)
  collecting ... collected 1 item
  
  tests.py::test_regular_sum FAILED                                        [100%]
  
  =================================== FAILURES ===================================
  _______________________________ test_regular_sum _______________________________
  
      def test_regular_sum():
  *       assert mypack.f(2, 1) == 3 (glob)
  E       assert 2 == 3
  E        +  where 2 = <function f at *>(2, 1) (glob)
  E        +    where <function f at *> = mypack.f (glob)
  
  tests.py:4: AssertionError
  =========================== short test summary info ============================
  FAILED tests.py::test_regular_sum - assert 2 == 3
  ============================== 1 failed in *s =============================== (glob)
  unit: exit 1 (* seconds) /tmp/cramtests-*> pytest -v tests.py pid=* (glob)
    unit: FAIL code 1 (*=setup[*]+cmd[*] seconds) (glob)
    evaluation failed :( (* seconds) (glob)
  ERROR: Commits suggest minor increment, but checks imply major increment
  [3]
