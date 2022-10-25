import logging
log = logging.getLogger(__name__)

import asyncio
from platform import python_version
from pyrogram import Client, filters, __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('login') & filters.private & filters.incoming)
async def login(c, m):
    url = "https://doodstream.com/api-docs"
    buttons = [[InlineKeyboardButton("Auth URL", url=url)]]
    await m.reply_text(
        text="--**Follow The below steps to login**--\n\n    • Open [Dood stream](http://doodstream.com) and login to the account\n\n    • And then press the below button and copy the API Key and paste here in the format `/token xxxxxxx...`",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_message(filters.command('token') & filters.private & filters.incoming)
async def token(c, m):
    if len(m.command) == 2:
        cmd, api_key = m.text.split(' ')
        url = f"https://doodapi.com/api/account/info?key={api_key}"
        userdetails = requests.get(url).json()
        if userdetails['status'] == 403:
            text = "Send me the correct token"
        elif userdetails['status'] == 200:
            await c.db.update_credential_status(m.from_user.id,  api_key)
            text = "--**Your Details:**--\n\n"
            text += f"**Email:** {userdetails['result']['email']}\n" if 'email' in userdetails['result'] else ""
            text += f"**Balance:** {userdetails['result']['balance']}\n" if 'balance' in userdetails['result'] else ""   
            text += f"**Storage left:** {userdetails['result']['storage_left']}\n" if 'storage_left' in userdetails['result'] else ""
            text += f"**Premium Expiry:** {userdetails['result']['premim_expire']}\n" if 'premim_expire' in userdetails['result'] else "" 
        else:
            text = "Something Went wrong"
        await m.reply_text(text)
    else:
        await m.reply_text("Use this command with API KEY.\n**Example:** `/token 34095x5c0kj164vxxxxxx`", quote=True)


@Client.on_callback_query(filters.regex('^home$'))
@Client.on_message(filters.command('start') & filters.incoming & filters.private)
async def start(client, message):
    if getattr(message, 'data', False):
        send_message = message.message
        try: await message.answer()
        except: pass
    else:
        try: send_message = await message.reply('**Processing....**', quote=True)
        except Exception as e: return log.error(e)
           

    # Buttons
    buttons = [[
        InlineKeyboardButton('My Father 👨‍✈️', url="https://t.me/Ns_AnoNymouS"),
        InlineKeyboardButton('Help 💡', callback_data="help")
        ],[
        InlineKeyboardButton('About 📕', callback_data="about"),
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    text = client.tools.START.format(mention=message.from_user.mention)
    await send_message.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()

    # help text
    help_text = """**You need Help?? 😎**

✪ First use /login command and follow the steps given there.

✪ For uploading telegram files to your doodstream account forward me a tg file or video.

✪ For uploading links send me the link i will upload them using remote upload.

✪ For checking your files use command /myfiles.

✪ For checking active uploads use command /remote_actions.

✪ For checking your account status use command /status.
"""
    # creating buttons
    buttons = [[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('About 📕', callback_data='about')
        ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]

    # editing as help message
    await m.message.edit(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex('^about$'))
@Client.on_message(filters.command('help') & filters.incoming & filters.private)
async def about_cb(client, message):
    if getattr(message, 'data', False):
        send_message = message.message
        try: await message.answer()
        except: pass
    else:
        try: send_message = await message.reply('**Processing....**', quote=True)
        except Exception as e: return log.error(e)

    bot = await client.get_me()
    text = client.tools.ABOUT.format(
        BOT_MENTION=bot.mention,
        PYTHON_VERSION=python_version(),
        PYROGRAM_VERSION=__version__
    )
    buttons = [[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('Help 💡', callback_data='help')
        ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]

    # editing message
    await send_message.edit(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(client, callback):
    try:
        await callback.message.delete()
        await callback.message.reply_to_message.delete()
    except: pass


@Client.on_message(filters.private & filters.incoming)
async def token_check(client, message):
    api_key = await client.db.get_credential_status(message.from_user.id)
    if not api_key:
        return await message.reply("You didn't Authorize me yet. Use the command and login to your account", quote=True)
    await message.continue_propagation()