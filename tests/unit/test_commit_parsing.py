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

    def test_scope_may_include_underscore(self):
        p = AngularCommitParser()
        assert p.parse(
            RawCommit(sha='any sha', title='feat(any_scope): Message', body='')
        ) == Commit(sha='any sha', type='feat', scope='any_scope', breaking=False)

    def test_scope_may_include_dash(self):
        p = AngularCommitParser()
        assert p.parse(
            RawCommit(sha='any sha', title='feat(any-scope): Message', body='')
        ) == Commit(sha='any sha', type='feat', scope='any-scope', breaking=False)
