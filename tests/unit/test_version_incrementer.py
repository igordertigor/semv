import pytest
from semv.config import Config
from semv.increment import DefaultIncrementer, VersionIncrement, Commit


class TestIncrements:
    @pytest.fixture
    def vi(self):
        config = Config()
        return DefaultIncrementer(config.commit_types_minor, config.commit_types_patch, config.commit_types_skip)

    def test_all_skip(self, vi):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='chore', scope='any scope', breaking=False),
        ]
        assert vi.get_version_increment(commits) == VersionIncrement.skip

    def test_skip_and_patch(self, vi):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='fix', scope='any scope', breaking=False),
        ]
        assert vi.get_version_increment(commits) == VersionIncrement.patch

    def test_skip_and_feature(self, vi):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='feat', scope='any scope', breaking=False),
        ]
        assert vi.get_version_increment(commits) == VersionIncrement.minor

    def test_skip_and_breaking_perf(self, vi):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='perf', scope='any scope', breaking=True),
        ]
        assert vi.get_version_increment(commits) == VersionIncrement.major

    def test_skip_and_non_breaking_perf(self, vi):
        commits = [
            Commit(sha='any sha', type='test', scope='any scope', breaking=False),
            Commit(sha='any sha', type='perf', scope='any scope', breaking=False),
        ]
        assert vi.get_version_increment(commits) == VersionIncrement.patch
