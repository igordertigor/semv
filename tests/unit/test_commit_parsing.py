import pytest
from semv.interface import RawCommit, Commit
from semv import errors
from semv.parse import AngularCommitParser, InvalidCommitAction


class TestAngularCommitParser:
    def test_non_breaking(self):
        p = AngularCommitParser()
        assert p.parse(
            RawCommit(sha='any sha', title='feat(scope): Message', body='')
        ) == Commit(sha='any sha', type='feat', scope='scope', breaking=False)

    def test_breaking(self):
        p = AngularCommitParser()
        assert p.parse(
            RawCommit(
                sha='any sha',
                title='feat(scope): Message',
                body='BREAKING CHANGE: bla bla',
            )
        ) == Commit(sha='any sha', type='feat', scope='scope', breaking=True)

    def test_scope_may_include_underscore(self):
        p = AngularCommitParser()
        assert p.parse(
            RawCommit(sha='any sha', title='feat(any_scope): Message', body='')
        ) == Commit(
            sha='any sha', type='feat', scope='any_scope', breaking=False
        )

    def test_scope_may_include_dash(self):
        p = AngularCommitParser()
        assert p.parse(
            RawCommit(sha='any sha', title='feat(any-scope): Message', body='')
        ) == Commit(
            sha='any sha', type='feat', scope='any-scope', breaking=False
        )

    def test_no_scope(self):
        p = AngularCommitParser()
        assert p.parse(
            RawCommit(sha='any sha', title='feat: No scope', body='')
        ) == Commit(
            sha='any sha', type='feat', scope=':global:', breaking=False
        )

    def test_break_scope_with_no_parens(self):
        p = AngularCommitParser(InvalidCommitAction.error)
        with pytest.raises(errors.InvalidCommitFormat):
            p.parse(RawCommit(sha='any sha', title='feat-notscope:', body=''))
