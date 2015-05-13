# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('debugconfig')
    group.addoption('--variables', action='store', metavar='path',
                    default=None, help='path to test variables JSON file.')


@pytest.fixture(scope='session')
def variables(request):
    data = {}
    path = request.config.getoption('variables')
    if path is not None:
        with open(path) as f:
            data = json.load(f)
    return data
