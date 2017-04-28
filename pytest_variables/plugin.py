# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
import sys

import pytest

from pytest_variables import errors


def default(module, path):
    try:
        with open(path, 'rb') as f:
            return module.load(f)
    except TypeError as exc:
        # NOTE: python 3.2-3.5 json expects string,
        # so we should rely on system encoding.
        # This is fixed in newer versions.
        with open(path) as f:
            return module.load(f)


parser_table = {
    'json': ('json', default),
    'hjson': ('hjson', default),
    'yml': ('yaml', default),
    'yaml': ('yaml', default)}


def import_parser(path, import_type, parser_func):
    try:
        __import__(import_type)
        mod = sys.modules[import_type]
    except ImportError:
        sys.exit('{0} import error, please make sure that {0} is '
                 'installed'.format(import_type))
    return parser_func(mod, path)


def pytest_addoption(parser):
    group = parser.getgroup('debugconfig')
    group.addoption(
        '--variables',
        action='append',
        default=[],
        metavar='path',
        help='path to variables file.')


def pytest_configure(config):
    config._variables = {}
    for path in config.getoption('variables'):
        ext = os.path.splitext(path)[1][1:].lower() or 'json'
        try:
            variables = import_parser(path, *parser_table[ext])
            config._variables.update(variables)
        except KeyError:
            print("Could not find a parser for the file extension '{0}'. "
                  'Supported extensions are: {1}'.format(
                      ext, ', '.join(sorted(parser_table.keys()))))
            config._variables.update(
                import_parser(path, *parser_table['json']))
        except ValueError as e:
            raise errors.ValueError('Unable to parse {0}: {1}'.format(
                path, e))


@pytest.fixture(scope='session')
def variables(pytestconfig):
    """Provide test variables from a specified file"""
    return pytestconfig._variables
