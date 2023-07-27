from semv.increment import DefaultIncrementer, VersionIncrement, Commit


class TestIncrements:
    def test_all_skip(self):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='chore', scope='any scope', breaking=False),
        ]
        vi = DefaultIncrementer()
        assert vi.get_version_increment(commits) == VersionIncrement.skip
