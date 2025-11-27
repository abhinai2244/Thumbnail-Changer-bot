import os
from dotenv import load_dotenv

load_dotenv("config.env")

class Config:
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0)) if os.environ.get("LOG_CHANNEL") else None
    MAX_CONCURRENT_TASKS = int(os.environ.get("MAX_CONCURRENT_TASKS", 5))
