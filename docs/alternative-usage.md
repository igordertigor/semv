# Alternative usage

## As a `commit-msg` hook

You can use semv as a `commit-msg` hook to check commit messages before
committing them to version control. This will only validate the commit format
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


## As an automatic changelog generator

If your commits have useful messages beyond the type/scope labelling, you may
want to use them for generating a changelog. Because semv already parses commit
messages, version v2.4.0 introduced a feature to automatically generate
changelogs. To do so, run semv with the `--changelog` option. The commit will
be formatted in [Markdown](https://www.markdownguide.org) and will start by
listing breaking changes. After that changes are grouped by type (first types
that imply a major release, them types that imply a minor release, and finally
types that imply a patch release) and then by scope.

To make most out of the changelog feature, use the default types. Other types
are supported, but the formatting is less nice. Keep in mind that commits are
grouped by type and scope&mdash;this allows you to incrementally write the
changelog with your commits. Keeping that in mind will also help you decide on
the wording for your commit messages. For example, this changelog:
```markdown
# New features
- changelog:
  - Internal commit representation of summary attributes
  - Add command for creating changelog with --changelog
  - Markdown formatting of changelog
  - Supports breaking changes (multiple per commit)
  - Group commits by scope
- commit-parsing: Include commit summary
```
Is much nicer than this changelog:
```markdown
# New features
- General: Commit supports summary stuff
- command: Initial draft for changelog command
- parse: Include commit summary when parsing
- changelog:
  - Changelog properly formatted except breaking change comments
  - Support breaking changes
  - group commits by scope
```
In fact, they both refer to the same commit history.

Starting with v2.5.0, changelogs can be exported in two different formats:
1. *pretty*: This is what you get if you just use the `--changelog` option. You
   can also select it explicitly by setting `--changelog=pretty`. The examples
   above also use this format.
2. *json*: Can be selected by setting `--changelog=json` and will result in a
   json-formatted changelog.

Note: You can rewrite past commits using `git rebase -i` *if you haven't pushed
them to a remote yet or if you can force-push to the remote*.
