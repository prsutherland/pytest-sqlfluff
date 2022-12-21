"""
pytest plugin to use sqlfluff to enable format checking of sql files.
"""
import pathlib
import subprocess
import sys

import pytest


HISTKEY = "sqlfluff/mtimes"
CONF_KEY = "_sqlfluffmtimes"


def pytest_addoption(parser):
    """Set up argparse(r) and ini parsing for pytest-sqlfluff"""
    group = parser.getgroup("sqlfluff")
    group.addoption(
        "--sqlfluff",
        action="store_true",
        help="enable sql format checking with sqlfluff",
    )

    parser.addini(
        "sqlfluff",
        help="'enabled' or 'disabled' to turn sqlfluff linting on or off.",
    )


def pytest_collect_file(path, parent):
    """Determine if file should be tested by pytest-sqlfluff"""
    config = parent.config
    if path.ext == ".sql" and config.option.sqlfluff:
        return SQLFluffFile.from_parent(parent, path=pathlib.Path(path))
    return None


def pytest_configure(config):
    """Initialize pytest-sqlfluff given the pytest configuration"""
    # load cached mtimes at session startup
    sqlfluff_ini = config.inicfg.get("sqlfluff", "disabled").strip().lower()
    if sqlfluff_ini not in ("enabled", "disabled"):
        raise ValueError(
            "'sqlfluff' option in pytest ini config must be either "
            "'enabled' or 'disabled'"
        )

    if sqlfluff_ini == "enabled":
        config.option.sqlfluff = True

    if config.option.sqlfluff and hasattr(config, "cache"):
        setattr(config, CONF_KEY, config.cache.get(HISTKEY, {}))
    config.addinivalue_line(
        "markers", "sqlfluff: enable sql format checking with sqlfluff"
    )


def pytest_unconfigure(config):
    """Finish/deactivate pytest-sqlfluff after tests are done."""
    # save cached mtimes at end of session
    if hasattr(config, CONF_KEY):
        config.cache.set(HISTKEY, getattr(config, CONF_KEY))


class SQLFluffFile(pytest.File):
    """File that sqlfluff will run on."""

    def collect(self):
        """Create a PyLintItem for the File."""
        yield SQLFluffItem.from_parent(parent=self, name="SQLFLUFF")


class SQLFluffItem(pytest.Item):
    """sqlfluff test running class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_marker("sqlfluff")
        self._sqlfluffmtime = None

    def setup(self):
        pytest.importorskip("sqlfluff")
        mtimes = getattr(self.config, CONF_KEY, {})
        self._sqlfluffmtime = self.fspath.mtime()
        old = mtimes.get(str(self.fspath), 0)
        if self._sqlfluffmtime == old:
            pytest.skip("file(s) previously passed sqlfluff format checks")

    def runtest(self):
        cmd = [sys.executable, "-m", "sqlfluff", "lint"]

        cmd.append(str(self.fspath))
        try:
            subprocess.run(
                cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True
            )
        except subprocess.CalledProcessError as error:
            raise SQLFluffError(error) from error

        mtimes = getattr(self.config, CONF_KEY, {})
        mtimes[str(self.fspath)] = self._sqlfluffmtime

    def repr_failure(self, excinfo, style=None):
        if excinfo.errisinstance(SQLFluffError):
            return excinfo.value.args[0].stdout
        return super().repr_failure(excinfo, style=style)

    def reportinfo(self):
        return (self.fspath, -1, "SQLFluff format check")


class SQLFluffError(Exception):
    """Raised when sqlfluff subprocess has a non-zero exit code"""
