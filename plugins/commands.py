import logging
logger = logging.getLogger(__name__)

import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyrogram.errors import UserBannedInChannel, UserNotParticipant, ChannelPrivate, ChatAdminRequired, FloodWait 
from translation import Translation
from config import Config


@Client.on_message(filters.private & filters.incoming)
async def fore(c, m):
    try:
        chat = await c.get_chat_member(-1001221642755, m.from_user.id)
        if chat.status == "kicked":
            await m.reply("You are Banned 😝", quote=True)
            m.stop_propagation()
    except UserBannedInChannel:
        return await m.reply("Hai you made a mistake so you are banned from channel so you are banned from me too 😜")
    except UserNotParticipant:
        button = [[InlineKeyboardButton('join Updates channel 🥰', url='https://t.me/Ns_bot_updates')]]
        markup = InlineKeyboardMarkup(button)
        return await m.reply(
            "Hai bro,\n\n"
            "**You must join my channel for using me.**\n\n"
            "Press this button to join now 👇",
            parse_mode='markdown',
            reply_markup=markup)
    m.continue_propagation()

@Client.on_message(filters.text & filters.private & filters.incoming)
async def text(c, m):
      if m.from_user.id in Config.LOGIN:
         if m.text == Config.Password:
            Config.LOGIN.remove(m.from_user.id)
            Config.OWNER.append(m.from_user.id)
            await m.reply_text(text="From now you will receive feedbacks. Untill this bot restart.  If you want to get feedbacks permanently add your id in config vars")
         if m.text != Config.Password:
            Config.LOGIN.remove(m.from_user.id)
            await m.reply_text(text="**Incorrect Password ⚠️**", parse_mode="markdown")
      if m.from_user.id in Config.feedback:
         button = [[
                   InlineKeyboardButton("Yes", callback_data="yes"),
                   InlineKeyboardButton("No", callback_data="cancel")
                  ]]
         markup = InlineKeyboardMarkup(button)
         await m.reply_text(text="Are you sure to send this feedback",
                            reply_markup=markup,
                            quote=True)
      try:
          if m.reply_to_message.text == "Send me the reply text":
             id = Config.SEND[0]
             await c.send_message(chat_id=int(id), text=m.text.markdown, parse_mode="markdown")
             Config.SEND.remove(id)
             await c.send_message(chat_id=m.chat.id, text="Notified successfully")
      except:
          pass

@Client.on_message(filters.command(["start"]))
async def start(c, m):
      button = [
          [
              InlineKeyboardButton("Feedback", callback_data="feedback"),
              InlineKeyboardButton("Rules", callback_data="rules"),
          ],
          [
              InlineKeyboardButton("About", callback_data="about"),
              InlineKeyboardButton("Login", callback_data="login")
          ]
      ]
      markup = InlineKeyboardMarkup(button)
      await m.reply_text(text=Translation.START.format(m.from_user.first_name),
                         disable_web_page_preview=True,
                         quote=True,
                         reply_markup=markup)
