# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

pytest_plugins = "pytester",


def run(testdir, variables='{"foo":"bar"}'):
    path = testdir.makefile('.json', variables)
    return testdir.runpytest('--variables', path)


class TestVariables:

    def test_no_variables(self, testdir):
        testdir.makepyfile("""
            def test(variables):
                assert variables == {}
        """)
        result = testdir.runpytest()
        assert result.ret == 0

    def test_variables(self, testdir):
        testdir.makepyfile("""
            def test(variables):
                assert variables['foo'] == 'bar'
        """)
        result = run(testdir)
        assert result.ret == 0

    def test_invalid_json(self, testdir):
        testdir.makepyfile('def test(variables): pass')
        result = run(testdir, 'invalid')
        assert result.ret == 1
        result.stdout.fnmatch_lines(['*ValueError: *'])

    def test_key_error(self, testdir):
        testdir.makepyfile("""
            def test(variables):
                assert variables['bar'] == 'foo'
        """)
        result = run(testdir)
        assert result.ret == 1
        result.stdout.fnmatch_lines(['*KeyError: *'])
