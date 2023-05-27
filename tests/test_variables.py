# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

pytest_plugins = ("pytester",)


def pytest_generate_tests(metafunc):
    if "file_format" in metafunc.fixturenames:
        metafunc.parametrize("file_format", ["json", "hjson", "yaml", "toml"])


def run(testdir, file_format="json", variables=None, raw=False):
    variables = variables or [{"foo": "bar"}]
    args = []
    for i, v in enumerate(variables):
        if file_format == "hjson" and not raw:
            hjson = pytest.importorskip("hjson")
            v = hjson.dumps(v)
        elif file_format == "yaml" and not raw:
            yaml = pytest.importorskip("yaml")
            v = yaml.dump(v)
        elif file_format == "toml" and not raw:
            toml = pytest.importorskip("toml")
            v = toml.dumps(v)
        elif not raw:
            import json

            v = json.dumps(v)
        args.append("--variables")
        kwargs = {"{0}".format(i): v}
        args.append(testdir.makefile(file_format, **kwargs))
    args.append("-s")
    return testdir.runpytest(*args)


def test_missing_extension(testdir, recwarn):
    testdir.makepyfile(
        """
        def test(variables):
            assert variables['foo'] == 'bar'
    """
    )
    result = run(testdir, "")
    assert result.ret == 0
    assert len(recwarn) == 0


def test_no_variables(testdir):
    testdir.makepyfile(
        """
        def test(variables):
            assert variables == {}
    """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_unsupported_format(testdir, recwarn):
    testdir.makepyfile(
        """
        def test(variables):
            assert variables['foo'] == 'bar'
    """
    )
    result = run(testdir, "invalid")
    assert result.ret == 0
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert issubclass(w.category, UserWarning)
    assert "Could not find a parser" in str(w.message)


def test_variables_basic(testdir, file_format):
    testdir.makepyfile(
        """
        def test(variables):
            assert variables['foo'] == 'bar'
    """
    )
    result = run(testdir, file_format)
    assert result.ret == 0


def test_invalid_format(testdir, file_format):
    testdir.makepyfile("def test(variables): pass")
    result = run(testdir, file_format, ["invalid="], raw=True)
    assert result.ret == 3
    result.stderr.fnmatch_lines(["*ValueError: Unable to parse*"])


def test_key_error(testdir, file_format):
    testdir.makepyfile(
        """
        def test(variables):
            assert variables['bar'] == 'foo'
    """
    )
    result = run(testdir, file_format)
    assert result.ret == 1
    result.stdout.fnmatch_lines(["*KeyError: *"])


def test_multiple_variables(testdir, file_format):
    testdir.makepyfile(
        """
        def test(variables):
            assert variables['foo'] == 'bar'
            assert variables['bar'] == 'foo'
    """
    )
    result = run(testdir, file_format, variables=[{"foo": "bar"}, {"bar": "foo"}])
    assert result.ret == 0


def test_multiple_variables_override(testdir, file_format):
    testdir.makepyfile(
        """
        def test(variables):
            assert variables['foo'] == 'bar'
            assert variables['bar'] == 'foo'
    """
    )
    result = run(
        testdir, file_format, variables=[{"foo": "foo", "bar": "foo"}, {"foo": "bar"}]
    )
    assert result.ret == 0


def test_multiple_variables_merge_override(testdir, file_format):
    """Dictionaries merge when there are shared keys"""
    testdir.makepyfile(
        """
        def test(variables):
            assert variables['capabilities']['browser'] == 'Firefox'
            assert variables['capabilities']['browser_version'] == '53.0'
            assert variables['capabilities']['debug'] == 'true'
    """
    )
    result = run(
        testdir,
        file_format,
        variables=[
            {"capabilities": {"browser": "Firefox", "browser_version": "53.0"}},
            {"capabilities": {"debug": "true"}},
        ],
    )
    assert result.ret == 0


def test_multiple_variables_merge_not_override_lists(testdir, file_format):
    """no lists extension, last wins"""
    testdir.makepyfile(
        """
        def test(variables):
            assert variables['list'] == [4, 5]
            assert variables['foo']['bar'] == 'true'
    """
    )
    result = run(
        testdir,
        file_format,
        variables=[{"list": [1, 2, 3]}, {"list": [4, 5], "foo": {"bar": "true"}}],
    )
    assert result.ret == 0
