# Commit parsing

Commit parsing follows the logic of [python semantic release](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html) in the [AngularCommitParser](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html#semantic-release-commit-parser-angularcommitparser).
Specifically, every commit message should have the following structure:
```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```
Where items in angle brackets (`<` and `>`) are interpreted as "variable" and
will be explained below.

Commits that do not fit this format can not be handled by semv. However, you
can [configure](configuration.md) how semv behaves if it encounters an invalid
commit.

Commit parsing is the main way how semv determines a new release version.
However, semv allows using [additional checks](checks.md) to validate the
version increment determined by parsing commits.

*New*: Starting with version v2.2.0, you can now omit the scope.

## The `type` keyword

The `type` keyword is the most important part for semv. It allows semv to
determine if this should be a minor or patch version increment. In the default
configuration, the type "feat" will trigger a minor release and the types "fix"
and "perf" will trigger a patch release. Other valid types are "chore" (some
clean-up that needed to be done, e.g. to config or something), "test" (adding a
test separately), "docs" (changes to documentation), "ci" (modifications to
continuous integration setup), "refactor", and "style". However, these other
types *will not trigger a new version*.

## The `scope` keyword

Is parsed but not used at the moment (version v2.2.0).

*New*: Starting with version v2.2.0, you can now omit the scope. As a result, a
commit message like "fix: General overhaul" is now valid.

## The `body` and `footer`

These are currently only parsed for lines that start with `BREAKING CHANGE: `.
If any such line is found, semv will trigger a major release.

## Which commits are parsed?

In order to determine the next version, all commits since the last version tag
(any tag of the form vX.Y.Z) are parsed.
If the current commit is a merge commit, then all branches that lead into it
are parsed and semv will analyze all commits that are not included in the last
version tag. For example
```
    v1.3.1
a ---> b ---> c ---> d
 \                  /
  \                /
   e -----------> f
```
In this case, commit `b` was tagged as version v1.3.1. If we call semv on
commit `d`, which merges the branch `e->f->d` into the "main" branch
`a->b->c->c`, the semv will analyze commits `b`, `d`, `e`, `f`.
Note that this isn't the case by default for [python semantic
release](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html).
