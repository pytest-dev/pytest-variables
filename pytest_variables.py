# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
import sys
import importlib

import pytest


def default(module, file):
    return module.load(file)

parser_table = []
# file extension name, import name, function 
parser_table.append(["json",    "json",     default])
parser_table.append(["hjson",   "hjson",    default])
parser_table.append(["yaml",    "yaml",     default])


def pytest_addoption(parser):
    group = parser.getgroup('debugconfig')
    group.addoption(
        '--variables',
        action='append',
        default=[],
        metavar='path',
        help='path to test variables JSON/HJSON/YAML file.')


@pytest.fixture(scope='session')
def variables(request):
    """Provide test variables from a JSON file or HJSON/YAML files if installed"""
    data = {}
    for path in request.config.getoption('variables'):
        extension = os.path.splitext(path)[1].replace(".","").lower()
        for row in range(len(parser_table)):
            if extension in parser_table[row][0]:
                try:
                    mod = importlib.import_module(parser_table[row][1])
                except ImportError:
                    sys.exit("{0} import error, please make sure that {0} is installed"
                             .format(parser_table[row][1]))
                with open(path) as f:
                    data.update(parser_table[row][2](mod, f))
                break
    return data