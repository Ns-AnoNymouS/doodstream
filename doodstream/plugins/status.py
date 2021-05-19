import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command(status) & filters.private & filters.incoming)
async def status(c, m):
    await m.reply_text()
