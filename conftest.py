import pytest

from app import create_app
from app.models import db


@pytest.fixture
def app():
    return create_app('test')


@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()

# pytest --cov-report term-missing --cov=app

