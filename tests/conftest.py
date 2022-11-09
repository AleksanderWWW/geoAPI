import pytest

from api import app


@pytest.fixture
def myapp():
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app


@pytest.fixture()
def client(myapp):
    return app.test_client()
