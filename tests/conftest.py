import os

import pytest
from alembic.command import upgrade
from alembic.config import Config
from database.database import SQLALCHEMY_DATABASE_URI, session


@pytest.fixture(scope="session")
def app():
    from app.main import create_app
    app = create_app()
    return app


@pytest.fixture(autouse=True)
def clear_db():
    file = SQLALCHEMY_DATABASE_URI.split('sqlite:///')[1]
    if os.path.isfile(file):
        os.remove(file)

    config = Config("alembic.ini")
    upgrade(config, "head")
    yield

    session.close_all()
    os.remove(file)


@pytest.fixture
def client(app):
    """A test client for the app."""
    app.testing = True
    return app.test_client()
