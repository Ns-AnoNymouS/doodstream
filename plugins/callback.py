import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply 
from pyrogram.errors import UserBannedInChannel, UserNotParticipant
from config import Config
from translation import Translation
from .commands import start 


@Client.on_callback_query()
async def foe(c, m):
    try:
        chat = await c.get_chat_member(-1001221642755, m.from_user.id)
        if chat.status == "kicked":
            await m.message.edit(text="You are Banned 😝")
            m.message.stop_propagation()
    except UserBannedInChannel:
        return await m.message.edit("Hai you made a mistake so you are banned from channel"
                                    " so you are banned from me too 😜")
    except UserNotParticipant:
        button = [[InlineKeyboardButton('join Updates channel 🥰', url='https://t.me/Ns_bot_updates')]]
        markup = InlineKeyboardMarkup(button)
        return await m.message.edit(
            "Hai bro,\n\n"
            "**You must join my channel for using me.**\n\n"
            "Press this button to join now 👇",
            parse_mode='markdown',
            reply_markup=markup)
    m.message.continue_propagation()


@Client.on_callback_query(filters.regex('^feedback'))
async def feedback_cb(c, m):
      Config.feedback.append(m.from_user.id)
      button = [[InlineKeyboardButton("cancel", callback_data="cancel")]]
      markup = InlineKeyboardMarkup(button)
      await m.message.edit("Send your feed back here I will notify the admin.", reply_markup=markup)

@Client.on_callback_query(filters.regex('^cancel'))
async def cancel_cb(c, m):
      if m.from_user.id in Config.feedback:
         Config.feedback.remove(m.from_user.id)
      if m.from_user.id in Config.LOGIN:
         Config.LOGIN.remove(m.from_user.id)
      button = [[
                InlineKeyboardButton("Feedback", callback_data="feedback"),
                InlineKeyboardButton("Rules", callback_data="rules"),
                InlineKeyboardButton("Login", callback_data="login"),
                ],
                [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Share", url="tg://share?url=Hey%20Friend%20Here%20is%20some%20of%20useful%20bots%0A%0A**NS%20BOT%20LIST**%0A%0A@uploadpro_Nsbot%0A@convert_Ns_bot%0A@Renamer_Ns_bot%0A@File_to_link_Nsbot%0A@Postdeleter_NsBot%0A@Gdrive_upload_Nsbot%0A@leech_NsBot%0A@Autoforward_Nsbot%0A@feedback_Nsbot")
               ]]
      markup = InlineKeyboardMarkup(button)
      await m.message.edit(text=Translation.START.format(m.from_user.first_name),
                            disable_web_page_preview=True,
                            reply_markup=markup)

@Client.on_callback_query(filters.regex('^back'))
async def back_cb(c, m):
      button = [[
                InlineKeyboardButton("Feedback", callback_data="feedback"),
                InlineKeyboardButton("Rules", callback_data="rules"),
                InlineKeyboardButton("Login", callback_data="login"),
                ],
                [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Share", url="tg://share?url=Hey%20Friend%20Here%20is%20some%20of%20useful%20bots%0A%0A**NS%20BOT%20LIST**%0A%0A@uploadpro_Nsbot%0A@convert_Ns_bot%0A@Renamer_Ns_bot%0A@File_to_link_Nsbot%0A@Postdeleter_NsBot%0A@Gdrive_upload_Nsbot%0A@leech_NsBot%0A@Autoforward_Nsbot%0A@feedback_Nsbot")
               ]]
      markup = InlineKeyboardMarkup(button)
      await m.message.edit(text=Translation.START.format(m.from_user.first_name),
                            disable_web_page_preview=True,
                            reply_markup=markup)

@Client.on_callback_query(filters.regex('^rules'))
async def rules_cb(c, m):
      button = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
      markup = InlineKeyboardMarkup(button)
      await m.message.edit(text=Translation.RULES,
                           reply_markup=markup)

@Client.on_callback_query(filters.regex('^login'))
async def login_cb(c, m):
      Config.LOGIN.append(m.from_user.id)
      button = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
      markup = InlineKeyboardMarkup(button)
      await m.message.edit(text=Translation.LOGIN,
                           reply_markup=markup)
       
@Client.on_callback_query(filters.regex('^yes'))
async def yes_cb(c, m):                     
      Config.feedback.remove(m.from_user.id)
      feedtext = str(m.message.reply_to_message.text) + f"\n\nName: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nID: `{m.from_user.id}`"
      button = [[InlineKeyboardButton("Reply", callback_data=f"reply+{m.from_user.id}")]]
      markup = InlineKeyboardMarkup(button)
      for i in Config.OWNER:
          await c.send_message(chat_id=int(i),
                               text=feedtext,
                               reply_markup=markup)
      await m.message.edit("Feedback sent successfully. Hope you will get reply soon")
      button = [[
                InlineKeyboardButton("Feedback", callback_data="feedback"),
                InlineKeyboardButton("Rules", callback_data="rules"),
                InlineKeyboardButton("Login", callback_data="login"),
                ],
                [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Share", url="tg://share?url=Hey%20Friend%20Here%20is%20some%20of%20useful%20bots%0A%0A**NS%20BOT%20LIST**%0A%0A@uploadpro_Nsbot%0A@convert_Ns_bot%0A@Renamer_Ns_bot%0A@File_to_link_Nsbot%0A@Postdeleter_NsBot%0A@Gdrive_upload_Nsbot%0A@leech_NsBot%0A@Autoforward_Nsbot%0A@feedback_Nsbot")
               ]]
      markup = InlineKeyboardMarkup(button)
      await c.send_message(text=Translation.START.format(m.from_user.first_name),
                           disable_web_page_preview=True,
                           parse_mode="markdown",
                           reply_markup=markup)

@Client.on_callback_query(filters.regex('^reply'))
async def reply_cb(c, m):
      id = m.data.split("+")[1]
      Config.SEND.append(id)
      await c.send_message(chat_id=m.message.chat.id, text="Send me the reply text", reply_markup=ForceReply())

@Client.on_callback_query(filters.regex('^about'))
async def about_cb(c, m):
      button = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
      markup = InlineKeyboardMarkup(button)
      await m.message.edit(text=Translation.ABOUT, disable_web_page_preview=True, reply_markup=markup)
