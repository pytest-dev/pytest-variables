# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
import sys

import json
import pytest

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
        extention = os.path.splitext(path)[1]
        if extention in {".hjson", ".HJSON"}:
            try:
                import hjson
            except ImportError:
                sys.exit("hjson import error, please make sure hjson is installed")
            with open(path) as f:
                data.update(hjson.load(f))
        elif extention in {".yaml", ".YAML"}:
            try:
                import yaml
            except ImportError:
                sys.exit("yaml import error, please make sure pyyaml is installed")
            with open(path) as f:
                data.update(yaml.load(f))
        else:
            with open(path) as f:
                data.update(json.load(f))
    return data