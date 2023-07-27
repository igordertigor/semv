from semv.increment import DefaultIncrementer, VersionIncrement, Commit


class TestIncrements:
    def test_all_skip(self):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='chore', scope='any scope', breaking=False),
        ]
        vi = DefaultIncrementer()
        assert vi.get_version_increment(commits) == VersionIncrement.skip

    def test_skip_and_patch(self):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='fix', scope='any scope', breaking=False),
        ]
        vi = DefaultIncrementer()
        assert vi.get_version_increment(commits) == VersionIncrement.patch

    def test_skip_and_feature(self):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='feat', scope='any scope', breaking=False),
        ]
        vi = DefaultIncrementer()
        assert vi.get_version_increment(commits) == VersionIncrement.minor

    def test_skip_and_breaking_perf(self):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='perf', scope='any scope', breaking=True),
        ]
        vi = DefaultIncrementer()
        assert vi.get_version_increment(commits) == VersionIncrement.major

    def test_skip_and_non_breaking_perf(self):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='perf', scope='any scope', breaking=False),
        ]
        vi = DefaultIncrementer()
        assert vi.get_version_increment(commits) == VersionIncrement.patch
