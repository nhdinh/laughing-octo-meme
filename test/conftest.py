import pytest

from app.app import create_app


@pytest.fixture
def test_client():
    app = create_app()
    app.debug = True

    return app.test_client()
