This test checks one of the main ideas of Stephan Bönnemann's talk: If the previous version's tests fail when running against a new version, then that version is likely a major version.

  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in /tmp/cramtests-4c2pe3yx/test_old_tests_on_new_version.t/.git/
  [master (root-commit) c21010a] docs(readme): Add readme
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
  .pkg: _optional_hooks> python /home/ingo/code/semv/.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True setuptools.build_meta
  .pkg: get_requires_for_build_sdist> python /home/ingo/code/semv/.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True setuptools.build_meta
  .pkg: build_sdist> python /home/ingo/code/semv/.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True setuptools.build_meta
  unit: install_package> python -I -m pip install --force-reinstall --no-deps /tmp/cramtests-4c2pe3yx/test_old_tests_on_new_version.t/.tox/.tmp/package/1/mypack-0.0.0.tar.gz
  unit: commands[0]> pytest tests.py
  ============================= test session starts ==============================
  platform linux -- Python 3.8.10, pytest-7.4.0, pluggy-1.2.0
  cachedir: .tox/unit/.pytest_cache
  rootdir: /tmp/cramtests-4c2pe3yx/test_old_tests_on_new_version.t
  collected 1 item
  
  tests.py .                                                               [100%]
  
  ============================== 1 passed in 0.00s ===============================
  .pkg: _exit> python /home/ingo/code/semv/.venv/lib/python3.8/site-packages/pyproject_api/_backend.py True setuptools.build_meta
    unit: OK (4.88=setup[4.76]+cmd[0.11] seconds)
    congratulations :) (4.91 seconds)

Commit
  $ git add src/mypack.py tests.py tox.ini pyproject.toml
  $ git commit -m "feat(mypack): Initial implementation"
  [master 98671c6] feat(mypack): Initial implementation
   4 files changed, 22 insertions(+)
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
  [master 4d58202] chore(semv): Add semv config
   1 file changed, 3 insertions(+)

Introduce a breaking change
  $ echo "def f(x, y):" > src/mypack.py
  $ echo "    return x * y" >> src/mypack.py
  $ git add src/mypack.py
  $ git commit -m 'feat(mypack): Multiplications are cooler'
  [master e646b93] feat(mypack): Multiplications are cooler
   1 file changed, 1 insertion(+), 1 deletion(-)
  $ semv
  unit: install_deps> python -I -m pip install pytest
  unit: install_package> python -I -m pip install --force-reinstall --no-deps /tmp/cramtests-4c2pe3yx/test_old_tests_on_new_version.t/dist/mypack-1.0.1.dev2+ge646b93-py3-none-any.whl
  unit: commands[0]> pytest -v tests.py
  ============================= test session starts ==============================
  platform linux -- Python 3.8.10, pytest-7.4.0, pluggy-1.2.0 -- /tmp/cramtests-4c2pe3yx/tmp/tmpaiw4fh43/.tox/unit/bin/python
  cachedir: .tox/unit/.pytest_cache
  rootdir: /tmp/cramtests-4c2pe3yx/tmp/tmpaiw4fh43
  collecting ... collected 1 item
  
  tests.py::test_regular_sum FAILED                                        [100%]
  
  =================================== FAILURES ===================================
  _______________________________ test_regular_sum _______________________________
  
      def test_regular_sum():
  >       assert mypack.f(2, 1) == 3
  E       assert 2 == 3
  E        +  where 2 = <function f at 0x7fee04aa1280>(2, 1)
  E        +    where <function f at 0x7fee04aa1280> = mypack.f
  
  tests.py:4: AssertionError
  =========================== short test summary info ============================
  FAILED tests.py::test_regular_sum - assert 2 == 3
  ============================== 1 failed in 0.01s ===============================
  unit: exit 1 (0.12 seconds) /tmp/cramtests-4c2pe3yx/tmp/tmpaiw4fh43> pytest -v tests.py pid=2592421
    unit: FAIL code 1 (1.65=setup[1.53]+cmd[0.12] seconds)
    evaluation failed :( (1.68 seconds)
  ERROR: Commits suggest minor increment, but checks imply major increment
  [3]
