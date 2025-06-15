from decouple import config, Csv
from dotenv import load_dotenv

load_dotenv(override=True)

DEBUG = config("DEBUG", default=False, cast=bool)
TELEGRAM_API_TOKEN = config("TELEGRAM_API_TOKEN")
TELEGRAM_ADMIN_IDS = config("TELEGRAM_ADMIN_IDS", cast=Csv(int)) or []
TELEGRAM_LOGGER_CHANNEL_ID = config("TELEGRAM_LOGGER_CHANNEL_ID", cast=int, default=0)
TELEGRAM_WEBHOOK_SECRET_KEY = config("TELEGRAM_WEBHOOK_SECRET_KEY")
TELEGRAM_WEBHOOK_HOST = config("TELEGRAM_WEBHOOK_HOST")
SQLALCHEMY_DATABASE_URL = (
    "mariadb+pymysql://portableuser:portablepass@localhost:3306/portabledb"
)
UVICORN_PORT = config("UVICORN_PORT", cast=int)
UVICORN_SSL_CERTFILE = config("UVICORN_SSL_CERTFILE", default="")
UVICORN_SSL_KEYFILE = config("UVICORN_SSL_KEYFILE", default="")
