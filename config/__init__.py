from os import environ
from models.user import UsersModel


class Config:
    SECRET_KEY = "CRAG"


class DevelopmentConfig(Config):
    DEBUG = True
    EGINE_URI = 'mysql://root:' + environ['passmaria'] + '@localhost'
    # * EGINE_URI = 'mysql://root:@localhost'
    DB_NAME = 'cruddb'
    SQLALCHEMY_DATABASE_URI = f'{EGINE_URI}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TABLE_VALIDATE_TOKEN = UsersModel
