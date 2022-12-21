"""
Fixtures for testing pyteset-sqlfluff
"""
from textwrap import dedent
from pytest import fixture


@fixture
def sqlfluff_project(testdir):
    """Fixture to setup a bare sqlfluff project in `testdir`"""
    testdir.makepyprojecttoml(
        dedent(
            """
            [tool.sqlfluff.core]
            dialect = "postgres"
            """
        )
    )
    testdir.makefile(".sql", "SELECT bar FROM foo").write("\n", mode="a")

    return testdir


pytest_plugins = "pytester"  # pylint: disable=invalid-name
