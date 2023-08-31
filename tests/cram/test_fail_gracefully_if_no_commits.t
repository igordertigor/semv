We need to run semv in a git repository.
  $ bash "$TESTDIR"/setup.sh
  Initialized empty Git repository in */.git/ (glob)
  [master (root-commit) *] docs(readme): Add readme (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 README.md

We now have a (non working) initial version v0.0.0 (note however, that this is
not standard and you might rather want to pick v1.0.0).
  $ semv
  WARNING: No changes for new version
  [1]
We will now add a few commits and then get a new version.
  $ echo "print('Hello')" > myscript.py
  $ git add myscript.py
  $ git commit -m 'feat(myscript): Print a message'
  [master *] feat(myscript): Print a message (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 myscript.py
  $ echo "print('Hello world!')" > myscript.py
  $ git add myscript.py
  $ git commit -m 'fix(myscript): Better message printed'
  [master *] fix(myscript): Better message printed (glob)
   1 file changed, 1 insertion(+), 1 deletion(-)

We now have two commits: The first implements a new feature, the second one
fixes the initial implementation. Let's assume we want to perform a release
now. We can print the new version (without writing anything yet) by running semv:
  $ semv
  v0.1.0 (no-eol)
As you can see, the output has no final newline character. That is because the
intended usage of semv would be to cause a new version tag like so:
  $ git tag $(semv)
This illustrates a core feature of semv: It will not perform any modifications
to your system.

  $ semv
  WARNING: No changes for new version
  [1]

Now let's add a commit that has an invalid message
  $ echo "This tool just greets the world" >> README.md
  $ git add README.md
  $ git commit -m 'readme: Add some more info about our tool'
  [master *] readme: Add some more info about our tool (glob)
   1 file changed, 1 insertion(+)
  $ git tag
  v0.0.0
  v0.1.0
  $ semv
  WARNING: Commit * has invalid type readme (glob)
  WARNING: No changes for new version
  [1]
