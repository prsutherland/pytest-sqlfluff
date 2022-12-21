"""
Tests for pytest-sqlfluff
"""
from pytest import Testdir


def test_help_message(testdir):
    """pytest should include our params in `pytest --help` output."""
    result = testdir.runpytest(
        "--help",
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "sqlfluff:",
            "*--sqlfluff*enable sql format checking with sqlfluff",
        ]
    )


def test_sqlfluff_params(sqlfluff_project: Testdir):
    """pytest should accept our fixture params and test sql files."""

    # run pytest with the following cmd args
    result = sqlfluff_project.runpytest("--sqlfluff", "-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*test_sqlfluff_params.sql::SQLFLUFF PASSED*",
        ]
    )

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_sqlfluff_ini_setting_enabled(sqlfluff_project):
    """pytest should test sql files if enabled in tox.ini."""
    sqlfluff_project.makeini(
        """
        [pytest]
        sqlfluff = enabled
        """
    )

    result = sqlfluff_project.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*test_sqlfluff_ini_setting_enabled.sql::SQLFLUFF PASSED*",
        ]
    )

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_sqlfluff_ini_setting_disabled(sqlfluff_project):
    """pytest should NOT test sql files if disabled in tox.ini."""
    sqlfluff_project.makeini(
        """
        [pytest]
        sqlfluff = disabled
        """
    )

    result = sqlfluff_project.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "collecting ... collected 0 items",
        ]
    )

    # make sure that that we get a '5' exit code for the testsuite (NO TESTS COLLECTED)
    assert result.ret == 5


def test_fixture_overrides_sqlfluff_ini(sqlfluff_project):
    """
    pytest should test sql files if disabled in tox.ini
    but --sqlfluff param is used.
    """
    sqlfluff_project.makeini(
        """
        [pytest]
        sqlfluff = disabled
        """
    )

    # run pytest with the following cmd args
    result = sqlfluff_project.runpytest("--sqlfluff", "-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*test_fixture_overrides_sqlfluff_ini.sql::SQLFLUFF PASSED*",
        ]
    )

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_noop(sqlfluff_project):
    """pytest not use the pytest-sqlfluff plugin if not enabled."""

    result = sqlfluff_project.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "collecting ... collected 0 items",
        ]
    )

    # make sure that that we get a '5' exit code for the testsuite (NO TESTS COLLECTED)
    assert result.ret == 5


def test_sqlfluff_ini_setting_bad_input(sqlfluff_project):
    """If the user misconfigures sqlfluff in tox.ini, a clear error should be raised"""

    sqlfluff_project.makeini(
        """
        [pytest]
        sqlfluff = invalid_input
        """
    )

    result = sqlfluff_project.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stderr.fnmatch_lines(
        [
            "*ValueError: 'sqlfluff' option in pytest ini config must be either "
            "'enabled' or 'disabled'",
        ]
    )

    # make sure that that we get a '3' exit code for the testsuite (INTERNAL ERROR)
    assert result.ret == 3
