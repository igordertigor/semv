This example will run through a typical scenario of using semv. As this is a
script, we will need to perform all code changes using echo commands, which is
kind of awkward, but it should be sufficient for testing.

We need to run semv in a git repository.
  $ git init
  Initialized empty Git repository in */.git/ (glob)
  $ echo "This is the readme" > README.md
  $ git add README.md
  $ git commit -m 'docs(readme): Add readme'
  [master (root-commit) *] docs(readme): Add readme (glob)
   1 file changed, 1 insertion(+)
   create mode 100644 README.md
  $ git tag v0.0.0

We now have a (non working) initial version v0.0.0 (note however, that this is
not standard and you might rather want to pick v1.0.0). We will now add a few
commits and then get a new version.
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

We now have to commits: The first implements a new feature, the second one
fixes the initial implementation. Let's assume we want to perform a release
now. We can print the new version (without writing anything yet) by running semv:
  $ semv
  v0.1.0 (no-eol)
As you can see, the output has no final newline character. That is because the
intended usage of semv would be to cause a new version tag like so:
  $ git tag $(semv)
This illustrates a core feature of semv: It will not perform any modifications
to your system.

Let's add another commit:
  $ echo "This tool just greets the world" >> README.md
  $ git add README.md
  $ git commit -m 'docs(readme): Add some more info about our tool'
  [master *] docs(readme): Add some more info about our tool (glob)
   1 file changed, 1 insertion(+)
As we can see, this new commit doesn't really add any functionality, but rather
just updates the documentation. We don't want to create a new version for this.
And indeed, semv won't do that.
  $ git tag
  v0.0.0
  v0.1.0
  $ semv
  WARNING: No changes for new version
  [1]
Instead semv returns with a status code of 1. Use can make use of this
behaviour when performing automatic releases and cancel the release process
accoringly. Also note, that the warning message is written to stderr, so if you
accidentally ran `git tag $(semv)`, git would just print the tags.
