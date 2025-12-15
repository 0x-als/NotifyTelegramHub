import os

from dotenv import load_dotenv

load_dotenv(".env")

# Connect to telegram bot and telegram api
telegram_config = {
    "telegram_token_api": os.getenv("TELEGRAM_TOKEN"),
}

# Connect postgresql
database_config = {
    "user": os.getenv("DATABASE_USER"),
    "password": os.getenv("DATABASE_PASSWORD"),
    "host": os.getenv("DATABASE_HOST"),
    "database": os.getenv("DATABASE_NAME"),
    "port": os.getenv("DATABASE_PORT"),
}
