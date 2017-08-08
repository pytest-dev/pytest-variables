pytest-variables
================

pytest-variables is a plugin for pytest_ that provides variables to
tests/fixtures as a dictionary via a file specified on the command line.

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/pytest-dev/pytest-variables/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-variables.svg
   :target: https://pypi.python.org/pypi/pytest-variables/
   :alt: PyPI
.. image:: https://img.shields.io/travis/pytest-dev/pytest-variables.svg
   :target: https://travis-ci.org/pytest-dev/pytest-variables/
   :alt: Travis
.. image:: https://img.shields.io/github/issues-raw/pytest-dev/pytest-variables.svg
   :target: https://github.com/pytest-dev/pytest-variables/issues
   :alt: Issues
.. image:: https://img.shields.io/requires/github/pytest-dev/pytest-variables.svg
   :target: https://requires.io/github/pytest-dev/pytest-variables/requirements/?branch=master
   :alt: Requirements

Requirements
------------

You will need the following prerequisites in order to use pytest-variables:

- Python 2.7, 3.6, PyPy, or PyPy3
- pytest 2.6 or newer

Installation
------------

To install pytest-variables:

.. code-block:: bash

  $ pip install pytest-variables

Additional formats
------------------

The following optional formats are supported, but must be explicitly installed
as they require additional dependencies:

Human JSON
~~~~~~~~~~

`Human JSON`_ is a configuration file format that caters to humans and helps
reduce the errors they make. To install Human JSON support:

.. code-block:: bash

  $ pip install pytest-variables[hjson]

YAML
~~~~

YAML_ is a human friendly data serialization standard for all programming
languages. To install YAML support:

.. code-block:: bash

  $ pip install pytest-variables[yaml]

Specifying variables
--------------------

Use the `--variables` command line option one or more times to specify paths to
files containing your variables:

.. code-block:: bash

  $ pytest --variables firefox-53.json --variables windows-10.json


with the following contents for the ``firefox-53.json`` file:

.. code-block:: json

  {
    "capabilities": {
      "browser": "Firefox",
      "browser_version": "53.0"
    }
  }

and another file named ``windows-10.json`` with:

.. code-block:: json

  {
    "capabilities": {
      "os": "Windows",
      "os_version": "10",
      "resolution": "1280x1024"
    }
  }

you'll get the merged version of your variables:

.. code-block:: json

  {
    "capabilities": {
      "browser": "Firefox",
      "browser_version": "53.0",
      "os": "Windows",
      "os_version": "10",
      "resolution": "1280x1024"
    }
  }

If multiple files are specified then they will be applied in the order they
appear on the command line. When duplicate keys with non dictionary_ values
are encountered, the last to be applied will take priority.

Accessing variables
-------------------

With a JSON variables file such as:

.. code-block:: json

  {
    "foo": "bar",
    "bar": "foo"
  }

Specify the `variables` funcarg to make the variables available to your tests.
The contents of the files are made available as a dictionary_:

.. code-block:: python

  def test_foo(self, variables):
      assert variables['foo'] == 'bar'
      assert variables.get('bar') == 'foo'
      assert variables.get('missing') is None

Resources
---------

- `Release Notes`_
- `Issue Tracker`_
- Code_

.. _pytest: http://pytest.org
.. _Human JSON: http://hjson.org
.. _YAML: http://yaml.org
.. _dictionary: https://docs.python.org/tutorial/datastructures.html#dictionaries
.. _Release Notes:  http://github.com/pytest-dev/pytest-variables/blob/master/CHANGES.rst
.. _Issue Tracker: http://github.com/pytest-dev/pytest-variables/issues
.. _Code: http://github.com/pytest-dev/pytest-variables
