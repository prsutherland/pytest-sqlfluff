# -*- coding: utf-8 -*-

import pathlib
import subprocess
import sys

import pytest


HISTKEY = "sqlfluff/mtimes"


def pytest_addoption(parser):
    group = parser.getgroup("sqlfluff")
    group.addoption(
        "--sqlfluff", action="store_true", help="enable sql format checking with sqlfluff"
    )


def pytest_collect_file(path, parent):
    config = parent.config
    if path.ext == ".sql" and config.option.sqlfluff:
        return SQLFluffFile.from_parent(parent, path=pathlib.Path(path))


def pytest_configure(config):
    # load cached mtimes at session startup
    if config.option.sqlfluff and hasattr(config, "cache"):
        config._sqlfluffmtimes = config.cache.get(HISTKEY, {})
    config.addinivalue_line("markers", "sqlfluff: enable sql format checking with sqlfluff")


def pytest_unconfigure(config):
    # save cached mtimes at end of session
    if hasattr(config, "_sqlfluffmtimes"):
        config.cache.set(HISTKEY, config._sqlfluffmtimes)


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

    def setup(self):
        pytest.importorskip("sqlfluff")
        mtimes = getattr(self.config, "_sqlfluffmtimes", {})
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
        except subprocess.CalledProcessError as e:
            raise SQLFluffError(e)

        mtimes = getattr(self.config, "_sqlfluffmtimes", {})
        mtimes[str(self.fspath)] = self._sqlfluffmtime

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(SQLFluffError):
            return excinfo.value.args[0].stdout
        return super(SQLFluffError, self).repr_failure(excinfo)

    def reportinfo(self):
        return (self.fspath, -1, "SQLFluff format check")


class SQLFluffError(Exception):
    pass
