from utils import env

SQLALCHEMY_DATABASE_URL = env("SQLALCHEMY_DATABASE_URL", "")
