# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
import sys
import pytest


def default(module, path):
    return module.load(path)


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


@pytest.fixture(scope='session')
def variables(request):
    """Provide test variables from a specified file"""
    data = {}
    for path in request.config.getoption('variables'):
        ext = os.path.splitext(path)[1][1:].lower()
        with open(path) as f:
            try:
                data.update(import_parser(f, *parser_table[ext]))
            except (TypeError, KeyError, ValueError):
                print("Could not find a parser for the file extension '{0}'. "
                      'Supported extensions are: {1}'.format(
                          ext, ', '.join(sorted(parser_table.keys()))))
                data.update(import_parser(f, *parser_table['json']))
    return data
