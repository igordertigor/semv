from semv.interface import RawCommit, Commit
from semv.parse import AngularCommitParser


class TestAngularCommitParser:
    def test_non_breaking(self):
        p = AngularCommitParser()
        assert p.parse(
            RawCommit(sha='any sha', title='feat(scope): Message', body='')
        ) == Commit(sha='any sha', type='feat', scope='scope', breaking=False)
    def test_breaking(self):
        p = AngularCommitParser()
        assert p.parse(
            RawCommit(sha='any sha', title='feat(scope): Message', body='BREAKING CHANGE: bla bla')
        ) == Commit(sha='any sha', type='feat', scope='scope', breaking=True)
