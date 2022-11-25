import nox


@nox.session
def pytest_and_mypy(session: nox.Session) -> None:
    session.install("poetry")
    session.run("poetry", "install")

    session.run("mypy", "pycooldown")
    session.run(
        "poetry",
        "run",
        "python",
        "-m",
        "pytest",
        "--cov=pycooldown/",
        "--cov-report=xml",
    )


@nox.session
def flake8(session: nox.Session) -> None:
    session.install("flake8")
    session.run("flake8")


@nox.session
def black(session: nox.Session) -> None:
    session.install("black")
    session.run("black", ".", "--check")


@nox.session
def isort(session: nox.Session) -> None:
    session.install("isort")
    session.run("isort", ".", "--check")
