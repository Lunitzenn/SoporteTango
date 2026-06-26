import pytest

from app import create_app
from app.models import db


@pytest.fixture
def app(tmp_path):
    test_db_path = tmp_path / 'test.db'
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{test_db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret',
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()
