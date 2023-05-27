# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
import sys
import warnings
import io

import pytest
from functools import reduce

from pytest_variables import errors


def default(module, path, loader):
    with io.open(path, "r", encoding="utf8") as f:
        try:
            return module.load(f, Loader=getattr(module, loader))
        except (AttributeError, TypeError):  # Module is not yaml or no loader
            return module.load(f)


variables_key = pytest.StashKey[dict]()

parser_table = {
    "json": ("json", default),
    "hjson": ("hjson", default),
    "yml": ("yaml", default),
    "yaml": ("yaml", default),
    "toml": ("toml", default),
}


def import_parser(path, import_type, parser_func, loader=None):
    try:
        __import__(import_type)
        mod = sys.modules[import_type]
    except ImportError:
        sys.exit(
            "{0} import error, please make sure that {0} is "
            "installed".format(import_type)
        )
    return parser_func(mod, path, loader)


def pytest_addoption(parser):
    parser.addini(
        "yaml_loader",
        default="FullLoader",
        help="Which loader to use when parsing yaml",
    )
    group = parser.getgroup("debugconfig")
    group.addoption(
        "--variables",
        action="append",
        default=[],
        metavar="path",
        help="path to variables file.",
    )


def _merge(a, b, path=None):
    """merges b and a configurations.
    Based on http://bit.ly/2uFUHgb
    """
    if path is None:
        path = []

    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                # b wins
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def pytest_configure(config):
    config.stash[variables_key] = {}
    paths = config.getoption("variables")
    loader = config.getini("yaml_loader")
    for path in paths:
        ext = os.path.splitext(path)[1][1:].lower() or "json"
        try:
            import_type, parser_func = parser_table[ext]
            variables = import_parser(path, import_type, parser_func, loader)
        except KeyError:
            warnings.warn(
                UserWarning(
                    "Could not find a parser for the file extension '{0}'. "
                    "Supported extensions are: {1}".format(
                        ext, ", ".join(sorted(parser_table.keys()))
                    )
                )
            )
            variables = import_parser(path, *parser_table["json"])
        except ValueError as e:
            raise errors.ValueError("Unable to parse {0}: {1}".format(path, e))

        if not isinstance(variables, dict):
            raise errors.ValueError("Unable to parse {0}".format(path))

        reduce(_merge, [config.stash[variables_key], variables])


@pytest.fixture(scope="session")
def variables(pytestconfig):
    """Provide test variables from a specified file"""
    return pytestconfig.stash[variables_key]
