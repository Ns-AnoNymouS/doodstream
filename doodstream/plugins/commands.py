from ..tools.requests import req
from pyrogram import Client, filters
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
        userdetails = await req(url)
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


@Client.on_message(filters.command('start') & filters.incoming & filters.private)
async def start(c, m, cb=False):

    # start text
    text = f"""Hi {m.from_user.mention(style='md')}

I am a doodstream bot to maintain your [doodstream](https://doodstream.com) account.

I can upload tg files to your doodstream account too. Check help button for more help.

**Maintained By:** [Anonymous](https://t.me/Ns_AnoNymouS)
"""

    # Buttons
    buttons = [[
        InlineKeyboardButton('My Father 👨‍✈️', url="https://t.me/Ns_AnoNymouS"),
        InlineKeyboardButton('Help 💡', callback_data="help")
        ],[
        InlineKeyboardButton('About 📕', callback_data="about"),
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    if cb:
        await m.answer()
        await m.message.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    else:
        await m.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons), quote=True,  disable_web_page_preview=True)


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
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('About 📕', callback_data='about')
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing as help message
    await m.message.edit(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    bot = await c.get_me()

    # about text
    about_text = f"""--**My Details:**--

🤖 𝐌𝐲 𝐍𝐚𝐦𝐞: {bot.mention(style='md')}
    
📝 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞: [Python 3](https://www.python.org/)

🧰 𝐅𝐫𝐚𝐦𝐞𝐰𝐨𝐫𝐤: [Pyrogram](https://github.com/pyrogram/pyrogram)

👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: [Anonymous](https://t.me/Ns_AnoNymouS)

📢 𝐂𝐡𝐚𝐧𝐧𝐞𝐥: [NS BOT UPDATES](https://t.me/Ns_bot_updates)

👥 𝐆𝐫𝐨𝐮𝐩: [Ns BOT SUPPORT](https://t.me/Ns_Bot_supporters)
"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('Help 💡', callback_data='help')
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing message
    await m.message.edit(
        text=about_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


@Client.on_callback_query(filters.regex('^home$'))
async def home_cb(c, m):
    await m.answer()
    await start(c, m, cb=True)


@Client.on_message(filters.private & filters.incoming)
async def token_check(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    if not api_key:
        return await m.reply_text("You didn't Authorize me yet. Use the command and login to your account", quote=True)
    await m.continue_propagation()
