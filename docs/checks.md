# Checks

## Running previous version's tests on current version's code

One of the main risks with automatic semantic versioning is the risk accidentally mark a breaking change as a minor or patch release.
Unfortunately, it is quite easy to forget to include the `BREAKING CHANGE: ` marker.
[Stephan Bönnemann](https://www.youtube.com/watch?v=tc2UgG5L7WM) therefore suggests running the tests of the previous version against a new release candidate.
