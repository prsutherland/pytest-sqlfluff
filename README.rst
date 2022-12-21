===============
pytest-sqlfluff
===============

.. image:: https://img.shields.io/pypi/v/pytest-sqlfluff.svg
    :target: https://pypi.org/project/pytest-sqlfluff
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-sqlfluff.svg
    :target: https://pypi.org/project/pytest-sqlfluff
    :alt: Python versions

.. image:: https://github.com/prsutherland/pytest-sqlfluff/actions/workflows/ci-flow.yml/badge.svg?branch=main
    :target: https://github.com/prsutherland/pytest-sqlfluff/actions/workflows/ci-flow.yml?branch=main
    :alt: See Build Status on Github Workflows

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code Style: Black

A `pytest`_ plugin to use `sqlfluff`_ to enable format checking of sql files.

----


Features
--------

* Tests any sql files found in project.
* Leverages existing `sqlfluff`_ configurations.
* Skips unchanged sql files.


Requirements
------------

* Python 3.7+
* `sqlfluff`_ 1.0.0+


Installation
------------

You can install `pytest-sqlfluff` via `pip`_ from `PyPI`_::

    $ pip install pytest-sqlfluff


Usage
-----

Out of the box, you can run `pytest-sqlfluff` as argument to `pytest`_::

    $ pytest --sqlfluff
    ====================================== test session starts ======================================
    platform darwin -- Python 3.9.6, pytest-7.2.0, pluggy-1.0.0
    rootdir: /code/github.com/prsutherland/pytest-sqlfluff
    plugins: sqlfluff-0.1.0
    collected 1 item

    tests/file.sql .                                                                          [100%]

    ======================================= 1 passed in 0.45s =======================================

To configure your sqlfluff linting, use the standard `sqlfluff configuration`_ mechanisms. At the very
least, you'll likely need to set the dialect.::

    [sqlfluff]
    dialect = postgres
    ...




Contributing
------------
Contributions are very welcome. Tests can be run with `pytest`_, please ensure
the coverage at least stays the same before you submit a pull request.

To get started::

    $ git clone https://github.com/prsutherland/pytest-sqlfluff.git
    $ cd pytest-sqlfluff
    $ poetry install

Run tests::

    $ poetry run pytest

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-sqlfluff" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`file an issue`: https://github.com/prsutherland/pytest-sqlfluff/issues
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`sqlfluff`: https://docs.sqlfluff.com/en/stable/
.. _`sqlfluff configuration`: https://docs.sqlfluff.com/en/stable/configuration.html
