"""Nox sessions used locally and by the CI workflow.

    uvx nox -s tests          # mocked tests on every supported Python
    uvx nox -s qiskit         # mocked tests on every supported Qiskit release
    uvx nox -s live           # tests against the real MQSS service (needs MQSS_TOKEN)

The mocked tests replace the MQP REST API with an in-memory stand-in
(test/mock_mqp.py), so they need neither a token nor network access.
"""

import nox
from nox.sessions import Session

nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv"
nox.options.sessions = ["tests"]

PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]
QISKIT_VERSIONS = ["0.46.3", "1.0.2", "1.1.2", "1.2.4", "1.3.3", "1.4.2", "2.0.0"]
PYTEST_COV = ["--cov=mqss", "--cov-append", "--cov-report=xml", "--cov-report=term"]


def _install(session: Session, *extra: str) -> None:
    session.install("-e", ".", "pytest", "pytest-cov", "python-dotenv", *extra)


@nox.session(python=PYTHON_VERSIONS)
def tests(session: Session) -> None:
    """Run the mocked tests."""
    _install(session)
    session.run("pytest", "-m", "mock", *PYTEST_COV, *session.posargs)


@nox.session(python="3.11")
@nox.parametrize("qiskit", QISKIT_VERSIONS, ids=QISKIT_VERSIONS)
def qiskit(session: Session, qiskit: str) -> None:
    """Run the mocked tests against one Qiskit release."""
    _install(session, f"qiskit=={qiskit}")
    session.run("pytest", "-m", "mock", *PYTEST_COV, *session.posargs)


@nox.session(python="3.12")
def live(session: Session) -> None:
    """Run the tests against the real MQSS service; needs MQSS_TOKEN."""
    _install(session)
    session.run("pytest", "-m", "backend or job", *session.posargs)
