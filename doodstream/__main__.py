import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .config import Config
from pyrogram import Client
from pyromod import listen
from .database.database import Database


def main():
    plugins = dict(root="doodstream/plugins")
    app = Client("Dood-Stream",
                 bot_token=Config.BOT_TOKEN,
                 api_id=Config.API_ID,
                 api_hash=Config.API_HASH,
                 plugins=plugins,
                 workers=100)


    app.db = Database(Config.DATABASE_URL, 'Doodstream_NsBot')
    app.run()


if __name__ == "__main__":
    main()
