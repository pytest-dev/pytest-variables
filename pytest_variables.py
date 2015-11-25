# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import re
import pytest


def pytest_addoption(parser):
    group = parser.getgroup('debugconfig')
    group.addoption(
        '--variables',
        action='append',
        default=[],
        metavar='path',
        help='path to test variables JSON file.')


@pytest.fixture(scope='session')
def variables(request):
    """Provide test variables from a JSON file"""
    data = {}
    for path in request.config.getoption('variables'):
        with open(path) as f:
            data.update(json.loads(json_minify(f.read())))
    return data


def json_minify(string, strip_space=True):
    """
    A port of the `JSON-minify` utility to the Python language.
    Based on JSON.minify.js: https://github.com/getify/JSON.minify
    Allows for commenting in JSON files
    From: https://github.com/getify/JSON.minify/tree/python
    """
    
    tokenizer = re.compile('"|(/\*)|(\*/)|(//)|\n|\r')
    end_slashes_re = re.compile(r'(\\)*$')

    in_string = False
    in_multi = False
    in_single = False

    new_str = []
    index = 0

    for match in re.finditer(tokenizer, string):

        if not (in_multi or in_single):
            tmp = string[index:match.start()]
            if not in_string and strip_space:
                # replace white space as defined in standard
                tmp = re.sub('[ \t\n\r]+', '', tmp)
            new_str.append(tmp)

        index = match.end()
        val = match.group()

        if val == '"' and not (in_multi or in_single):
            escaped = end_slashes_re.search(string, 0, match.start())

            # start of string or unescaped quote character to end string
            if not in_string or (escaped is None or len(escaped.group()) % 2 == 0):  # noqa
                in_string = not in_string
            index -= 1  # include " character in next catch
        elif not (in_string or in_multi or in_single):
            if val == '/*':
                in_multi = True
            elif val == '//':
                in_single = True
        elif val == '*/' and in_multi and not (in_string or in_single):
            in_multi = False
        elif val in '\r\n' and not (in_multi or in_string) and in_single:
            in_single = False
        elif not ((in_multi or in_single) or (val in ' \r\n\t' and strip_space)):  # noqa
            new_str.append(val)

    new_str.append(string[index:])
    return ''.join(new_str)
