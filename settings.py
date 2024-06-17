from dotenv import load_dotenv

from utils import env

load_dotenv("./.env")

SQLALCHEMY_DATABASE_URL = env("SQLALCHEMY_DATABASE_URL", "")
