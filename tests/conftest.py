import pytest
from app import create_app


@pytest.fixture()
def app():
    application = create_app()
    application.config.update({
        "TESTING": True,
    })

    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
