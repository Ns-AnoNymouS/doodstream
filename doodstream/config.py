import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    OWNER = os.environ.get("OWNER_ID", [1337144652])
    DATABASE_URL = os.environ.get("DATABASE_URL", "")

