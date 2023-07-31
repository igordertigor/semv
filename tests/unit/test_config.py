from semv import config


class TestToml(object):
    def test_section_at_end(self):
        s = """
        [something.ignored]
        somekey = "Hello"

        [tool.semv]
        invalid_commit_action = "error"
        """
        assert config.Config.parse(s).invalid_commit_action == (
            config.InvalidCommitAction.error
        )

    def test_section_followed_by_other(self):
        s = """
        [something.ignored]
        somekey = "Hello"

        [tool.semv]
        invalid_commit_action = "error"

        [something.else.ignored]
        """
        assert config.Config.parse(s).invalid_commit_action == (
            config.InvalidCommitAction.error
        )

    def test_no_semv_config(self):
        s = """
        [something.ignored]

        [something.else.ignored]
        """
        assert config.Config.parse(s).invalid_commit_action == (
            config.InvalidCommitAction.warning  # Default
        )
