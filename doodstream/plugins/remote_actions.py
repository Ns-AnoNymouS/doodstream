import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('remote_actions))
async def actions(c, m):
    buttons = [[
    ]]
    await m.reply_text()
