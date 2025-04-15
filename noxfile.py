import nox

from nox.sessions import Session


@nox.session()
def test(session: Session):
    session.run("uv", "sync", external=True)
    session.run("pytest", "-v", "-s")
