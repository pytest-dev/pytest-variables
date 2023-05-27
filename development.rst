Development
===========

To contribute to `pytest-variables` you can use `Hatch <https://hatch.pypa.io/latest/>`_ to manage
a python virtual environment and `pre-commit <https://pre-commit.com/>`_ to help you with
styling and formatting.

To setup the virtual environment and pre-commit, run:

.. code-block:: bash

  $ hatch -e test run pre-commit install

If you're not using ``Hatch``, to install ``pre-commit``, run:

.. code-block:: bash

  $ pip install pre-commit
  $ pre-commit install


Automated Testing
-----------------

All pull requests and merges are tested in `GitHub Actions <https://docs.github.com/en/actions>`_
based on the workflows defined in ``.github/workflows``.

Running Tests
-------------

You will need `Tox <https://tox.wiki/en/latest/>`_ installed to run the tests
against the supported Python versions. If you're using ``Hatch`` it will be
installed for you.

With ``Hatch``, run:

.. code-block:: bash

  $ hatch -e test run tox

Otherwise, to install and run, do:

.. code-block:: bash

  $ pip install tox
  $ tox

Releasing a new version
-----------------------

Follow these steps to release a new version of the project:

#. Update your local master with the upstream master (``git pull --rebase upstream master``)
#. Create a new branch and update ``CHANGES.rst`` with the new version, today's date, and all changes/new features
#. Update ``pyproject.toml`` with the new version
#. Commit and push the new branch and then create a new pull request
#. Wait for tests and reviews and then merge the branch
#. Once merged, update your local master again (``git pull --rebase upstream master``)
#. Tag the release with the new release version (``git tag <new tag>``)
#. Push the tag (``git push upstream --tags``)
#. Done.
