# semv - A read-only semantic version commit parsing and validation tool

This package is inspired by a talk by [Stephan
Bönnemann](https://www.youtube.com/watch?v=tc2UgG5L7WM) as well as the package
[python semantic
release](https://python-semantic-release.readthedocs.io/en/latest/).
Both suggest parsing commit message to automatically create a new version number.
Although this is a great idea, I don't think that commit messages can be guaranteed to be of sufficiently high quality to be used for this.
Stephan's talk acknowledges this point and suggests strategies for automatically validating commit messages.
Unfortunately, these are not implemented in python semantic release.
In addition, python semantic release does a lot more than just versioning: It covers the full release process, including uploads to pypi or github releases.
As a result, running python semantic release can have quite a few unexpected side effects that might be difficult to undo.
I would prefer a tool that does the hard part of the automatic semantic versioning (parsing and validating commit messages) but doesn't have any side effects&mdash;the user should be free to use tags, variables, commits or whatever they like to represent new versions and the user should not be surprised by unexpected write operations.
I therefore wrote semv, a read-only semantic version commit parsing and validation tool.

## Installation and usage

You can install semv from pypi using

  $ pip install semv

If you are inside a git repository, you can use semv to print the semantic version that the current commit *should* recieve. E.g.

  $ semv
  v1.0.5 (no-eol)

Note that this will have not change anything about your repository. It is up to you to use the printed version. An example for using the printed version is given in semv's own [release workflow](https://github.com/igordertigor/semv/blob/master/.github/workflows/attempt-release.yml).

## Configuration

You can configure semv via the `pyproject.toml` config file. Here are the defaults:
```toml
[tool.semv]
invalid_commit_action = "warning"  # Could also be "error" or "skip"

[tool.types]
feat = "minor"
fix = "patch"
perf = "patch"
chore = "valid"
test = "valid"
docs = "valid"
ci = "valid"
refactor = "valid"
style = "valid"
```
