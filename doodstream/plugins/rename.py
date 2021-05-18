import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.progress_bar import humanbytes, TimeFormatter


@Client.on_callback_query(filters.regex('^rename'))
aaync def remame(c, m):
