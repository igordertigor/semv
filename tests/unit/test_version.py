from semv.interface import Version, VersionIncrement


class TestVersion:
    def test_major_increment(self):
        v = Version()
        inc = VersionIncrement.major
        assert str(v + inc) == 'v2.0.0'

    def test_minor_increment(self):
        v = Version()
        inc = VersionIncrement.minor
        assert str(v + inc) == 'v1.1.0'

    def test_patch_increment(self):
        v = Version()
        inc = VersionIncrement.patch
        assert str(v + inc) == 'v1.0.1'

    def test_from_string(self):
        assert str(Version.from_string('v3.2.5')) == 'v3.2.5'
