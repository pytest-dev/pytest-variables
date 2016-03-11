# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

import pytest

pytest_plugins = "pytester",


def pytest_generate_tests(metafunc):
    if 'file_format' in metafunc.fixturenames:
        metafunc.parametrize('file_format', ['', 'json', 'hjson', 'yaml'])


def run(testdir, file_format='json', variables=None):
    variables = variables or [{"foo": "bar"}]
    args = []
    for i, v in enumerate(variables):
        if file_format == 'hjson':
            hjson = pytest.importorskip('hjson')
            v = hjson.dumps(v)
        elif file_format == 'yaml':
            yaml = pytest.importorskip('yaml')
            v = yaml.dump(v)
        else:
            import json
            v = json.dumps(v)
        args.append('--variables')
        args.append(testdir.makefile('{0}.{1}'.format(i, file_format), v))
    return testdir.runpytest(*args)


def test_no_variables(testdir):
    testdir.makepyfile("""
        def test(variables):
            assert variables == {}
    """)
    result = testdir.runpytest()
    assert result.ret == 0


def test_unsupported_format(testdir):
    testdir.makepyfile("""
        def test(variables):
            assert variables['foo'] == 'bar'
    """)
    result = run(testdir, 'invalid')
    assert result.ret == 0


def test_variables_basic(testdir, file_format):
    testdir.makepyfile("""
        def test(variables):
            assert variables['foo'] == 'bar'
    """)
    result = run(testdir, file_format)
    assert result.ret == 0


def test_invalid_format(testdir, file_format):
    testdir.makepyfile('def test(variables): pass')
    result = run(testdir, file_format, ['invalid'])
    assert result.ret == 1
    if sys.version_info < (3, 5, 0):
        result.stdout.fnmatch_lines(['*ValueError: *'])
    else:
        result.stdout.fnmatch_lines(['*JSONDecodeError: *'])


def test_key_error(testdir, file_format):
    testdir.makepyfile("""
        def test(variables):
            assert variables['bar'] == 'foo'
    """)
    result = run(testdir, file_format)
    assert result.ret == 1
    result.stdout.fnmatch_lines(['*KeyError: *'])


def test_multiple_variables(testdir, file_format):
    testdir.makepyfile("""
        def test(variables):
            assert variables['foo'] == 'bar'
            assert variables['bar'] == 'foo'
    """)
    result = run(testdir, file_format, variables=[
        {'foo': 'bar'}, {'bar': 'foo'}])
    assert result.ret == 0


def test_multiple_variables_override(testdir, file_format):
    testdir.makepyfile("""
        def test(variables):
            assert variables['foo'] == 'bar'
            assert variables['bar'] == 'foo'
    """)
    result = run(testdir, file_format, variables=[
        {'foo': 'foo', 'bar': 'foo'},
        {'foo': 'bar'}])
    assert result.ret == 0
