import datetime
from ..config import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserBannedInChannel, UserNotParticipant


@Client.on_message(filters.private & filters.incoming)
async def force_sub(c, m):
    chat_id = m.from_user.id
    try:
        chat = await c.get_chat_member('Ns_bot_updates', m.from_user.id)
        if chat.status=='kicked':
            return await m.reply_text('😡 Hai you are kicked from my updates channel. So, you are not able to use me 😝',  quote=True)

    except UserBannedInChannel:
        return await m.reply_text("Hai you made a mistake so you are banned from channel so you are banned from me too 😜",  quote=True)

    except UserNotParticipant:
        button = [[InlineKeyboardButton('join Updates channel 🥰', url='https://t.me/Ns_bot_updates')]]
        markup = InlineKeyboardMarkup(button)
        return await m.reply_text(text="""Hai bro,\n\n**You must join my channel for using my bot.**\n\nPress this button to join now 👇""", parse_mode='markdown', reply_markup=markup, quote=True)

    except Exception as e:
        return await m.reply_text("Some thing went wrong🤔. Try again and if same issue occur contact [our group](https://t.me/Ns_Bot_supporters)", disable_web_page_preview=True, quote=True)

    if not await c.db.is_user_exist(chat_id):
        await c.db.add_user(chat_id)

    ban_status = await c.db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])).days > ban_status["ban_duration"]:
            await c.db.remove_ban(chat_id)
        else:
            banned_text = "--🛑 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗕𝗮𝗻𝗻𝗲𝗱 🛑--\n\n"
            banned_text += 'Banned Date: '
            banned_text += f"`{ban_status['banned_on']}`\n"
            banned_text += 'Banned Duration: '
            banned_text += f"{ban_status['ban_duration']} day(s)\n"
            banned_text += 'Reason: '
            banned_text += f"__**{ban_status['ban_reason']}**__\n\n"
            banned_text += f"if you think this is a mistake contact [𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬](https://t.me/Ns_AnoNymouS)"
            await m.reply_text(banned_text, quote=True)
            return
    await m.continue_propagation()

