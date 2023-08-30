You can run semv as a commit-msg hook:
  $ git init
  Initialized empty Git repository in */.git/ (glob)
  $ echo '#!/bin/bash' > .git/hooks/commit-msg
  $ echo 'semv --commit-msg $1' >> .git/hooks/commit-msg
  $ chmod u+x .git/hooks/commit-msg
  $ echo 'test' > README.md
  $ git add README.md
  $ git commit -m 'invalid message'
  ERROR: Invalid commit:  invalid message
  [1]
