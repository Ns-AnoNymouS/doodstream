import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

from .tools import Tools
from .config import Config
from pyrogram import Client
from pyromod import listen
from .database.database import Database


class NsBots(Client, Config):
    def __init__(self):
        super().__init__(
            name="Dood-Stream",
            bot_token=self.bot_token,
            api_id=self.api_id,
            api_hash=self.api_hash,
            plugins=dict(root="doodstream/plugins"),
            workers=100
        )
        self.active_downloads = dict()
        self.db = Database(self.database_url, 'Doodstream_Bot')
        self.tools = Tools(self)


    async def start(self):
        await super().start()
        me = await self.get_me()
        log.info(f'Your Doodstream bot was started in {me.first_name} ({me.username})')


    async def stop(self):
        await super().stop()
        log.info('Stopped your Doodstream bot')


if __name__ == "__main__":
    NsBots().run()
