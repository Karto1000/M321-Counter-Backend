import pytest

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_get_count(client):
    response = client.get("/count")
    assert response.status_code == 200
    assert int(response.text) == 0
    
    client.post("/increment")
    
    response = client.get("/count")
    assert response.status_code == 200
    assert int(response.text) == 1