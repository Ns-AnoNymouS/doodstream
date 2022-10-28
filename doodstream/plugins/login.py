from doodstream_api import DoodStream
from pyrogram import Client, filters

@Client.on_message(filters.command('login') & filters.private & filters.incoming)
async def login(client, message):
    dood = DoodStream()
    username = await client.ask(message.from_user.id, 'send your username')
    password = await client.ask(message.from_user.id, 'send your password')
    sts = await dood.login(username.text, password.text)
    if sts == 'otp_sent':
        otp = await client.ask(message.from_user.id, 'send the opt sent to your email.')
        sts = await dood.login(username.text, password.text, otp.text)
