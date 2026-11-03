import nox

from nox.sessions import Session


def run_tests(session: Session, qiskit: str, marker: str) -> None:
    """Install the requested Qiskit version and run the selected tests."""
    if session.python == "3.14" and tuple(map(int, qiskit.split("."))) < (2, 1):
        session.skip(
            "Python 3.14 uses Qiskit 2.1+; older releases require SymEngine <0.14, "
            "which has no Python 3.14 wheels."
        )
    session.run("uv", "sync", "--active", "--frozen", external=True)
    session.run("uv", "pip", "install", f"qiskit=={qiskit}", external=True)
    session.run("python", "-m", "pytest", "-v", "-s", "-m", marker, *session.posargs)


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
