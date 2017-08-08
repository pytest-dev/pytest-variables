Release Notes
-------------

**1.7.0 (2017-08-08)**

* Merge dictionaries in variables when multiple files are provided.

  * Thanks to `@davidemoro <https://github.com/davidemoro>`_ for the PR

**1.6.1 (2017-04-28)**

* Fix :code:`TypeError` when opening variables in Python 3.2-3.5

  * Thanks to `@kottenator <https://github.com/kottenator>`_ for the report

**1.6.0 (2017-04-25)**

* Open file in binary format to address incorrect encoding on Windows

  * Thanks to `@vgavro <https://github.com/vgavro>`_ for the PR

**1.5.1 (2017-03-01)**

* Removed unintentional print of variables

**1.5.0 (2017-03-01)**

* Moved parsing of variables to :code:`pytest_configure` and store as
  :code:`config._variables` so access is not limited to fixtures

**1.4.0 (2016-03-18)**

* Remove unsupported format message for files with no extension

  * Thanks to `@RibeiroAna <https://github.com/RibeiroAna>`_ for the PR

**1.3.0 (2015-12-15)**

* Add support for Human JSON and YAML formats

  * Thanks to `@the-ivan <https://github.com/the-ivan>`_ for the PR

* Add documentation for :code:`variables` fixture

  * Thanks to `@styro <https://github.com/styro>`_ for the PR

**1.2.0 (2015-07-29)**

* Require :code:`--variables` command line option for all variables files

**1.1.0 (2016-07-16)**

* Allow multiple variables files to be specified

**1.0.0 (2015-05-13)**

* Initial release
