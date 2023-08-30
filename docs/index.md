# Getting started

SEMV is a read-only semantic version commit parsing and validation tool. It is
intended to help with automatic versioning following a semantic version logic.

This package is inspired by a talk by [Stephan
Bönnemann](https://www.youtube.com/watch?v=tc2UgG5L7WM) as well as the package
[python semantic
release](https://python-semantic-release.readthedocs.io/en/latest/). Both
suggest parsing commit message to automatically create a new version number.
Although this is a great idea, I don't think that commit messages can be
guaranteed to be of sufficiently high quality to be used for this. Stephan's
talk acknowledges this point and suggests strategies for automatically
validating commit messages.

Unfortunately, these are not implemented in python semantic release. In
addition, python semantic release does a lot more than just versioning: It
covers the full release process, including uploads to pypi or github releases.
As a result, running python semantic release can have quite a few unexpected
side effects that might be difficult to undo.

I would prefer a tool that does the hard part of the automatic semantic
versioning (parsing and validating commit messages) but doesn't have any side
effects&mdash;the user should be free to use tags, variables, commits or
whatever they like to represent new versions and the user should not be
surprised by unexpected write operations. I therefore wrote semv, a read-only
semantic version commit parsing and validation tool.


## Installation and usage

You can install semv from pypi using
<!-- note how this is not indented. We don't want to run this in cram tests, as semv is already installed in the test directory -->
```
$ pip install semv
```

<!--
This is a markdown comment. However, the code block still runs in cram tests,
hence we use this as a setup block.
  $ git init
  * (glob)
  $ echo Content >> file
  $ git add file
  $ git commit -m "dummy commit"
  * (glob)
  * (glob)
  * (glob)
  $ git tag v1.0.4
  $ echo More content > file
  $ git commit -am "fix(file): other dummy commit but with tag"
  * (glob)
  * (glob)
-->

If you are inside a git repository, you can use semv to print the semantic
version that the current commit *should* receive. E.g.
```
  $ semv
  v1.0.5 (no-eol)
```
Here, and anywhere else in this documentation, the `$`-sign indicates an interactive command line prompt and doesn't need to be typed.
The `(no-eol)` tag will not be shown and is only intended to indicate that semv will not print a newline character. That means that you could use semv to create a version tag like this:
```
  $ git tag $(semv)
```

Note that semv itself will have not change anything about your repository. It is up to
you to use the printed version. An example for using the printed version is
given in semv's own [release
workflow](https://github.com/igordertigor/semv/blob/master/.github/workflows/attempt-release.yml).

Other usage patterns can be found in [alternative usage](alternative-usage.md),
for example using semv as a `commit-msg` hook to check commits before
committing them to version control.


## Understanding semantic versions

Semantic versions are version numbers that carry some basic information about
the content of the corresponding release. Semv aims to help with automatically
creating releases that have semantic versions. Specifically, semv will create
the main segment of a semantic version identifier: vX.Y.Z, where X is usually
referred to as the "major" version, Y is usually referred to as the "minor"
version and Z is usually referred to as the "patch" version. We will stick to
these names throughout this documentation because they are quite common.

Having three separate version numbers isn't in itself necessarily useful. However, in semantic versioning, these three separate numbers indicate different kinds of releases:

- A *major* release (i.e. one that increments the X component of the above
  version numbers) is a release that breaks previously existing functionality.
  In fact, this could be something as simple as removing a feature, but often it
  will rather be a change in the software's user interface.
- A *minor* release adds functionality. Typically, that would be a release that implements one or more new features.
- Finally, a *patch* release would not change functionality but includes an improvement in existing functionality. That would typically be bug-fixes and performance improvements.

Semantic versions are useful for consumers of a package: They can often
specify a range of versions e.g. ">=v1.3.0" and "<v3.0.0" to indicate that
they rely on a feature that was implemented in version v1.3.0 but they can't
work with a functionality or interface that was removed in version v3.0.0.
Note that this also signifies that they can live with the breaking change that
was introduced in v2.0.0.

Python's semantic versioning strategy further allows for qualifiers after the
core version identifier that mark things like post-releases or release
candidates. See [pep 440](https://peps.python.org/pep-0440/) for detail.


## Commit Parsing

In order to automatically calculate the next version, semv parses commit
messages (and potentially performs additional steps). That means that commit
messages should be [formatted in a particular way](commit_parsing.md): Each
commit message should start with a line of the form `type(scope): <short
description>`, where `type` would be a commit type like "feat" or "fix" and
"scope" would be the thing that was actually changed. For example, the commit
message "feat(parsing): Parsing can now handle foo as well" would describe a
commit that adds a new feature to the parsing component of your application.
At the moment (v1.4.5), semv doesn't parse the scope.

Below the first line, users can add a body (as is good practice with commit
messages in general). The body should be separated from the title by an empty
line. In order to detect breaking changes, semv will expect the body to start
with `BREAKING CHANGE: ` if the commit contains a breaking change.

In addition to commit parsing, semv can be [configured](configuration.md) to
also run additional checks to&mdash;for example&mdash;detect some forms of
breaking changes automatically.


## Configuration

In general, semv should have reasonable defaults. However, you can configure
semv via the `pyproject.toml` config file. Details of the configuration
options are [here](configuration.md).
