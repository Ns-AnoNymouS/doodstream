from doodstream_api import DoodStream


@Client.on_message(filters.command('login') & filters.private & filters.incoming)
async def login(client, message):
    dood = DoodStream()
    await dood.login('Ns_Anonymous', 'Naveen9329@')