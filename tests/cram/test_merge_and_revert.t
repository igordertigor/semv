  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in */.git/ (glob)
  [master (root-commit) *] docs(readme): Add readme (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 README.md

Write the config:
We want errors on invalid commits.
We want valid non-structured commits to be the ones that start with "Merge" and "Revert"
  $ echo "[tool.semv]" > pyproject.toml
  $ echo 'invalid_commit_action = "error"' >> pyproject.toml
  $ echo 'skip_commit_patterns = ["^Merge.*", "^Revert.*"]' >> pyproject.toml

Now create two commits and revert one:
  $ echo "change" >> README.md
  $ git add README.md
  $ git commit -m "fix(readme): Mislabeling to make this increment the version"
  [master *] fix(readme): Mislabeling to make this increment the version (glob)
   1 file changed, 1 insertion(+)
  $ echo "other change" >> README.md
  $ git add README.md
  $ git commit -m "docs(readme): Some change"
  [master *] docs(readme): Some change (glob)
   1 file changed, 1 insertion(+)
  $ git revert HEAD
  [master *] Revert "docs(readme): Some change" (glob)
   Date: * (glob)
   1 file changed, 1 deletion(-)
  $ git log HEAD~..HEAD
  commit * (glob)
  Author: tester <tester>
  Date:   * (glob)
  
      Revert "docs(readme): Some change"
      
      This reverts commit *. (glob)

We now have an invalid commit, but it matches our skip pattern
  $ semv
  v0.0.1 (no-eol)

Next, create a branch and merge it
  $ git checkout -b feature/test-merge-commit
  Switched to a new branch 'feature/test-merge-commit'
  $ echo "more change" >> README.md
  $ git add README.md
  $ git commit -m "fix(readme): Mislabel again to create version"
  [feature/test-merge-commit *] fix(readme): Mislabel again to create version (glob)
   1 file changed, 1 insertion(+)
  $ git checkout master
  Switched to branch 'master'
Merge with --no-ff to force a merge commit
  $ git merge --no-ff feature/test-merge-commit
  Merge made by the '*' strategy. (glob)
   README.md | 1 +
   1 file changed, 1 insertion(+)
  $ git log HEAD~..HEAD
  commit * (glob)
  Merge: * * (glob)
  Author: tester <tester>
  Date:   * (glob)
  
      Merge branch 'feature/test-merge-commit'
  
  commit * (glob)
  Author: tester <tester>
  Date:   * (glob)
  
      fix(readme): Mislabel again to create version
 $ semv
 v0.0.1 (no-eol)
