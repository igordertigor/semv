This test checks if commits from other branches are correctly takin into
consideration when creating a new version.

Setup:
  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in */.git/ (glob)
  [master (root-commit) *] docs(readme): Add readme (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 README.md

We now create two branches and merge the second first
  $ git checkout -b branch1
  Switched to a new branch 'branch1'
  $ echo "Change 1" >> README.md
  $ git commit -am "docs(readme): Commit from first branch"
  [branch1 *] docs(readme): Commit from first branch (glob)
   1 file changed, 1 insertion(+)
  $ echo "Change 2" >> README.md
  $ git commit -am "feat(readme): Fancy feature"
  [branch1 *] feat(readme): Fancy feature (glob)
   1 file changed, 1 insertion(+)
  $ git checkout master
  Switched to branch 'master'

  $ git checkout -b branch2
  Switched to a new branch 'branch2'
  $ echo "Change 3" >> README.md
  $ git commit -am "docs(readme): Commit from second branch"
  [branch2 *] docs(readme): Commit from second branch (glob)
   1 file changed, 1 insertion(+)
  $ git checkout master
  Switched to branch 'master'

  $ git merge branch2
  Updating *..* (glob)
  Fast-forward
   README.md | 1 +
   1 file changed, 1 insertion(+)
  $ semv
  WARNING: No changes for new version
  [1]

  $ git merge branch1
  Auto-merging README.md
  CONFLICT (content): Merge conflict in README.md
  Automatic merge failed; fix conflicts and then commit the result.
  [1]

Fix merge commit
  $ echo "This is the readme" > README.md
  $ echo "Change 1" >> README.md
  $ echo "Change 2" >> README.md
  $ echo "Change 3" >> README.md
  $ git add README.md
  $ git commit -m "Merge branch "
  [master *] Merge branch (glob)
  $ git status
  On branch master
  nothing to commit, working tree clean
  $ semv
  WARNING: Invalid commit: * Merge branch (glob)
  v0.1.0 (no-eol)
