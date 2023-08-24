# Checks

## Running previous version's tests on current version's code

One of the main risks with automatic semantic versioning is the risk
accidentally mark a breaking change as a minor or patch release. Unfortunately,
it is quite easy to forget to include the `BREAKING CHANGE: ` marker. [Stephan
Bönnemann](https://www.youtube.com/watch?v=tc2UgG5L7WM) therefore suggests
running the tests of the previous version against a new release candidate: If
the tests from the previous version fail on the new release candidate, then
that release candidate is likely a breaking change and should be a major
version.

This is currently only implemented for [tox](https://tox.wiki/en/latest/cli_interface.html#tox-run---installpkg):

### RunPreviousVersionsTestsTox
::: semv.hooks.RunPreviousVersionsTestsTox
