import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(env_path)


class Secrets:
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "localhost")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "mytestdb")
    DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{MYSQL_DB}"
    )
    EMAIL: str = os.getenv("EMAIL", "placeholder@gmail.com")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "placeholder_password")
    PRODUCTION: bool = True if os.getenv("PRODUCTION", "").lower() == "true" else False


secrets = Secrets()
