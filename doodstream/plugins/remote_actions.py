import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('remote_actions'))
async def actions(c, m, cb=False):
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/urlupload/slots?key={api_key}"
    list_uploads = f"https://doodapi.com/api/urlupload/list?key={api_key}"
    data = requests.get(url).json()
    remote_list = requests.get(list_uploads).json()

    reply_markup = None
    text = "--**Remote Upload:**--\n\n"
    text += f"**Total Slots:** {data['total_slots']}\n"
    text += f"**Used Slots:** {data['used_slots']}\n\n\n"
    if data['used_slots'] != 0:
        text += "--**Active Uploads:**--\n\n"
        for file in remote_list['result']:
            text += f"**🔗 Url:** {file['remote_url']}\n"
            text += f"**📊 Status:** {file['status']}\n\n\n"
        buttons = [[
            InlineKeyboardButton("🔄 Restart Errors", callback_data="action+restart_errors"),
            InlineKeyboardButton("🛑 Clear Errors", callback_data="action+clear_errors"),
            InlineKeyboardButton("🗑 Clear All", callback_data="action+clear_all")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
    if not cb:
        await m.reply_text(text=text, reply_markup=reply_markup, quote=True)
    else:
        await m.message.edit(text=text, reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^action'))
async def cb_action(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    cmd, act = m.data.split('+')
    url = f"https://doodapi.com/api/urlupload/actions?key={api_key}&{act}=1"
    requests.get(url).json()
    await actions(c, m, cb=True)
    
