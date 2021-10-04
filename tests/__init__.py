from datetime import timedelta

from werkzeug.security import generate_password_hash

from app.models import User, QrCode
from config import Config
from app import create_app
from app import db
import uuid
import pytest


class TestConfig(Config):
    TESTING = True
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # This will run Sqlite in memory
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=2)  # To test refresh tokens


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            assert app.config['ENV'] == "production"
            db.create_all()
            db.session.commit()
        yield client


@pytest.fixture
def client_with_data():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            assert app.config['ENV'] == "production"
            db.create_all()
            db.session.add(User(email='test@mail.com', password_hash=generate_password_hash('test_password')))
            db.session.add(QrCode(
                code_value='some_test_value1',
                name='test_name1',
                embedded_value='val1',
                user_id=1,
                stored_name=str(uuid.uuid4())))
            db.session.add(QrCode(
                code_value='some_test_value2',
                name='test_name2',
                embedded_value='val2',
                user_id=1,
                stored_name=str(uuid.uuid4())))
            db.session.add(QrCode(
                code_value='some_test_value3',
                name='test_name3',
                embedded_value='val3',
                user_id=1,
                stored_name=str(uuid.uuid4())))
            db.session.commit()
        yield client
