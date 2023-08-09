  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in */.git/ (glob)
  [master (root-commit) *] docs(readme): Add readme (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 README.md
  $ echo "More text" >> README.md
  $ git add README.md
  $ git commit -m 'docs(readme): update'
  [master *] docs(readme): update (glob)
   1 file changed, 1 insertion(+)

Case 1: No hooks
  $ semv
  WARNING: No changes for new version
  [1]

Case 2: Hook returns skip
  $ echo "[tool.semv.checks]" > pyproject.toml
  $ echo 'DummyVersionEstimator = {increment="skip"}' >> pyproject.toml
  $ semv
  Dummy version estimator called on version v0.0.0, increment skip
  WARNING: No changes for new version
  [1]

Case 3: Hook returns major version ~> Failure
  $ echo "[tool.semv.checks]" > pyproject.toml
  $ echo 'DummyVersionEstimator = {increment="major"}' >> pyproject.toml
  $ semv
  Dummy version estimator called on version v0.0.0, increment major
  ERROR: Commits suggest skip increment, but checks imply major increment
  [3]
