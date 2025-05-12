import nox

from nox.sessions import Session


@nox.session(python=False)
@nox.parametrize(
    "qiskit", ["0.46.3", "1.0.2", "1.1.2", "1.2.4", "1.3.3", "1.4.2", "2.0.0"]
)
def test(session: Session, qiskit: str) -> None:
    """Run the tests with different Qiskit versions."""
    session.run("rm", "-rf", ".venv", external=True)
    session.run("uv", "lock", "--upgrade-package", f"qiskit=={qiskit}", external=True)
    session.run("uv", "sync", external=True)
    session.run("uv", "run", "pytest", "-v", "-s", "-m", "backend", external=True)
