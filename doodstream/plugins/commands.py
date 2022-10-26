import logging
log = logging.getLogger(__name__)

import asyncio
from platform import python_version
from pyrogram import Client, filters, __version__
from doodstream_api import DoodStream, InvalidApiKey
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand 


@Client.on_message(filters.command('set_commands') & filters.private & filters.incoming)
async def set_commands(client, message):
    print(message.coo)
    if len(message.command) == 2:
        commands = message.command[1]
        bot_commands = []
        for command in commands.splitlines():
            bot_command, description = (x.strip() for x in command.split('-'))
            bot_commands.append(BotCommand(bot_command, description))
        await client.set_bot_commands(bot_commands)
    else:
        await client.set_bot_commands([
            BotCommand("start", "check whether bot alive or not"),
            BotCommand("login", "connect bot with your doodstream account"),
            BotCommand("token", "your api key to connect with doodstream"), 
            BotCommand("myfiles", "your doodstream account files."),
            BotCommand("remote_actions", "check remote uplaod status"),
            BotCommand("status", "check your account status")
        ])
    await message.reply("sucess")


@Client.on_message(filters.command('login') & filters.private & filters.incoming)
async def login(client, message):
    buttons = [[InlineKeyboardButton("API Key 🗝", url="https://doodstream.com/settings")]]
    try:
        await message.reply(
            text=client.tools.LOGIN,
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    except Exception as e: log.error(e)


@Client.on_message(filters.command('token') & filters.private & filters.incoming)
async def token(client, message):
    try: send_message = await message.reply(client.tools.PROCESSING, quote=True)
    except Exception as e: log.error(e)

    try:
        if len(message.command) == 2:
            api_key = message.command[1]
            doodstream = DoodStream(api_key)
            userdetails = await doodstream.accountInfo()
            if userdetails['status'] == 403:
                text = "Send me the correct token"
            elif userdetails['status'] == 200:
                await client.db.update_credential_status(message.from_user.id,  api_key)
                text = "--**Your Details:**--\n\n"
                text += f"**Email:** {userdetails['result']['email']}\n" if 'email' in userdetails['result'] else ""
                text += f"**Balance:** {userdetails['result']['balance']}\n" if 'balance' in userdetails['result'] else ""   
                text += f"**Storage left:** {userdetails['result']['storage_left']}\n" if 'storage_left' in userdetails['result'] else ""
                text += f"**Premium Expiry:** {userdetails['result']['premim_expire']}\n" if 'premim_expire' in userdetails['result'] else "" 
            else:
                log.info(userdetails)
                text = "Something Went wrong"
        else:
            text = "Use this command with API KEY.\n**Example:** `/token 34095x5c0kj164vxxxxxx`"
    except Exception as e: text = f"--Error:--\n\n{e}"
    
    try: await send_message.edit(text)
    except Exception as e: log.error(e)


@Client.on_callback_query(filters.regex('^home$'))
@Client.on_message(filters.command('start') & filters.incoming & filters.private)
async def start(client, message):
    if getattr(message, 'data', False):
        send_message = message.message
        try: await message.answer()
        except: pass
    else:
        try: send_message = await message.reply(client.tools.PROCESSING, quote=True)
        except Exception as e: return log.error(e)

    # creating start message buttons
    buttons = [[
        InlineKeyboardButton('My Father 👨‍✈️', url="https://t.me/Ns_AnoNymouS"),
        InlineKeyboardButton('Help 💡', callback_data="help")
        ],[
        InlineKeyboardButton('About 📕', callback_data="about"),
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    text = client.tools.START.format(mention=message.from_user.mention)

    # editing as start message
    try:
        await send_message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    except MessageNotModified: pass
    except Exception as e: log.error(e)


@Client.on_callback_query(filters.regex('^help$'))
@Client.on_message(filters.command('help') & filters.incoming & filters.private)
async def help(client, message):
    if getattr(message, 'data', False):
        send_message = message.message
        try: await message.answer()
        except: pass
    else:
        try: send_message = await message.reply(client.tools.PROCESSING, quote=True)
        except Exception as e: return log.error(e)

    # creating buttons for help
    buttons = [[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('About 📕', callback_data='about')
        ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]

    # editing as help message
    try:
        await send_message.edit(
            text=client.tools.HELP,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    except MessageNotModified: pass
    except Exception as e: log.error(e)


@Client.on_callback_query(filters.regex('^about$'))
@Client.on_message(filters.command('about') & filters.incoming & filters.private)
async def about_cb(client, message):
    if getattr(message, 'data', False):
        send_message = message.message
        try: await message.answer()
        except: pass
    else:
        try: send_message = await message.reply(client.tools.PROCESSING, quote=True)
        except Exception as e: return log.error(e)

    # getting about text ready
    bot = await client.get_me()
    text = client.tools.ABOUT.format(
        BOT_MENTION=bot.mention,
        PYTHON_VERSION=python_version(),
        PYROGRAM_VERSION=__version__
    )

    # Creating buttons 
    buttons = [[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('Help 💡', callback_data='help')
        ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]

    # editing as about message
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
