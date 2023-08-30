# Alternative usage

You can use semv as a `commit-msg` hook to check commit messages before
commiting them to version control. This will only validate the commit format
but not run additional checks. To run semv as a `commit-msg` hook, store the following in a file `.git/hooks/commit-msg`:
```bash
#!/bin/bash

semv --commit-msg $1
```
and make the file executable by running
```
  $ chmod u+x .git/hooks/commit-msg
```
Next time you commit an invalid commit message, git should give you an error.
