import os

from dotenv import load_dotenv

project_root = os.getcwd()
load_dotenv(os.path.join(project_root, '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = (os.environ.get('SQLALCHEMY_DATABASE_URI')
                               or 'sqlite:///' + os.path.abspath("database/database.db"))
