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
The `(no-eol)` tag will not be shown and is only intended to indicate that semv will not print a newline character. That means that you could use semv to create a version tag like this:
```
  $ git tag $(semv)
```

Note that semv itself will have not change anything about your repository. It is up to
you to use the printed version. An example for using the printed version is
given in semv's own [release
workflow](https://github.com/igordertigor/semv/blob/master/.github/workflows/attempt-release.yml).


## Understanding semantic versions

tbd

See [pep 440](https://peps.python.org/pep-0440/) for now.


## Commit Parsing

In order to automatically calculate the next version, semv parses commit messages (and potentially performs additional steps).
That means that commit messages should be [formatted in a particular
way](commit_parsing.md): Each commit message should start with a line of the form `type(scope): <short description>`, where `type` would be a commit type like "feat" or "fix" and "scope" would be the thing that was actually changed. For example, the commit message "feat(parsing): Parsing can now handle foo as well" would describe a commit that adds a new feature to the parsing component of your application. At the moment (v1.4.5), semv doesn't parse the scope.

Below the first line, users can add a body (as is good practice with commit messages in general). The body should be separated from the title by an empty line. In order to detect breaking changes, semv will expect the body to start with `BREAKING CHANGE: ` if the commit contains a breaking change.

In addition to commit parsing, semv can be [configured](configuration.md) to also run additional checks to&mdash;for example&mdash;detect some forms of breaking changes automatically.


## Configuration

In general, semv should have reasonable defaults.
However, you can configure semv via the `pyproject.toml` config file.
Details of the configuration options are [here](configuration.md).
