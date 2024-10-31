import nox
import os
from nox.sessions import Session

os.environ.update({"PDM_IGNORE_SAVED_PYTHON": "1"})

SRC_DIR = "mqp"
TEST_DIR = "test"

pylint_args = []
mypy_args = []


@nox.session(reuse_venv=True)
def test(session: Session):
    session.run("pdm", "install", "-G:all", external=True)
    session.run("pytest", "-v", "-s")
    # session.run("coverage", "run", f"--source={SRC_DIR}", "-m", "pytest")
    # session.run("coverage", "report", "-m")


@nox.session(reuse_venv=True)
def lint(session: Session):
    session.run("pdm", "install", "-G:all", external=True)
    session.run("pylint", SRC_DIR, TEST_DIR, *pylint_args)
    session.run("black", "--check", SRC_DIR, TEST_DIR)
    session.run("isort", "--check", SRC_DIR, TEST_DIR)


@nox.session(reuse_venv=True)
def typecheck(session: Session):
    session.run("pdm", "install", "-G:all", external=True)
    session.run("mypy", SRC_DIR, *mypy_args)
    session.run("mypy", TEST_DIR, *mypy_args)
