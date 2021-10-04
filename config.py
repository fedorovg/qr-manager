import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xad\n\x93\x11\xe9ul\xe8\xaf\xfar\x97\xddGIx'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or b'\x13\n]\x19\xe6\x98\x15\n\x8a\t\xbf\x02%\xae\x7f\xad'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    GENERATED_CODES_PATH = os.path.join(basedir, 'app', 'generated')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)