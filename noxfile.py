import nox

from nox.sessions import Session


def run_tests(session: Session, qiskit: str, marker: str) -> None:
    """Install the requested Qiskit version and run the selected tests."""
    session.run("rm", "-rf", ".venv", external=True)
    session.run("uv", "lock", "--upgrade-package", f"qiskit=={qiskit}", external=True)
    session.run("uv", "sync", external=True)
    session.run("uv", "run", "pytest", "-v", "-s", "-m", marker, external=True)


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"])
@nox.parametrize(
    "qiskit",
    ["1.2.4", "1.3.3", "1.4.2", "2.0.0", "2.1.0", "2.2.0", "2.3.0", "2.4.0", "2.5.2"],
)
def test_backend(session: Session, qiskit: str) -> None:
    """Run the tests with different Qiskit versions."""
    run_tests(session, qiskit, "backend")


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"])
@nox.parametrize(
    "qiskit",
    ["1.2.4", "1.3.3", "1.4.2", "2.0.0", "2.1.0", "2.2.0", "2.3.0", "2.4.0", "2.5.2"],
)
def test_job(session: Session, qiskit: str) -> None:
    """Run the tests with different Qiskit versions."""
    run_tests(session, qiskit, "job")
