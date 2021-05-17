import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .config import Config
from pyrogram import Client


def main():
    plugins = dict(root="plugins")
    app = Client("Dood-Stream",
                 bot_token=Config.TG_BOT_TOKEN,
                 api_id=Config.APP_ID,
                 api_hash=Config.API_HASH,
                 plugins=plugins,
                 workers=100)

    app.run()


if __name__ == "__main__":
    main()
