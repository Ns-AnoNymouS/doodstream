from doodstream_api import DoodStream
from pyrogram import Client, filters

@Client.on_message(filters.command('login') & filters.private & filters.incoming)
async def login(client, message):
    dood = DoodStream()
    await dood.login('Ns_Anonymous', 'Naveen9329@')