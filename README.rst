pytest-variables
================

pytest-variables is a plugin for `py.test <http://pytest.org>`_ that provides
variables to tests/fixtures as a dict via a JSON file specified on the command
line.

.. image:: https://img.shields.io/pypi/l/pytest-variables.svg
   :target: https://github.com/davehunt/pytest-variables/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-variables.svg
   :target: https://pypi.python.org/pypi/pytest-variables/
   :alt: PyPI
.. image:: https://img.shields.io/travis/davehunt/pytest-variables.svg
   :target: https://travis-ci.org/davehunt/pytest-variables/
   :alt: Travis
.. image:: https://img.shields.io/github/issues-raw/davehunt/pytest-variables.svg
   :target: https://github.com/davehunt/pytest-variables/issues
   :alt: Issues
.. image:: https://img.shields.io/requires/github/davehunt/pytest-variables.svg
   :target: https://requires.io/github/davehunt/pytest-variables/requirements/?branch=master
   :alt: Requirements

Requirements
------------

You will need the following prerequisites in order to use pytest-variables:

- Python 2.6, 2.7, 3.2, 3.3, 3.4 or PyPy
- py.test 2.4 or newer

Installation
------------

To install pytest-variables::

  pip install pytest-variables

Specifying variables
--------------------

Use the `--variables` command line option one or more times to specify paths to
JSON files containing your variables::

  py.test --variables foo.json --variables bar.json

If multiple files are specified then they will be applied in the order they
appear on the command line. When duplicates are encountered, the last
to be applied will take priority.

Accessing variables
-------------------

With a JSON variables file such as:

.. code-block:: json

  {
    "foo": "bar",
    "bar": "foo"
  }

Specify the `variables` funcarg to make the variables available to your tests.
The contents of the JSON are made available as a
`dictionary <https://docs.python.org/tutorial/datastructures.html#dictionaries>`_:

.. code-block:: python

  def test_foo(self, variables):
      assert variables['foo'] == 'bar'
      assert variables.get('bar') == 'foo'
      assert variables.get('missing') is None

Resources
---------

- `Issue Tracker <http://github.com/davehunt/pytest-variables/issues>`_
- `Code <http://github.com/davehunt/pytest-variables/>`_
