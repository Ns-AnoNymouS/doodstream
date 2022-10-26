class Text:


# The message that should be sent when user press about button or send /about command
# You can use some special Keyword specified below
#     BOT_FIRST: gives the bot first name
#     BOT_LAST: gives the bot last name
#     BOT_MENTION: gives the hyper link of bot with bot first name
#     PYROGRAM_VERSOIN: gives the pyrogram version in the format x.x.x  
#     PYTHON_VERSOIN: gives the python verion in the format x.x.x 
      ABOUT = """
--**My Details:**--

🤖 My Name: {BOT_MENTION}

📝 Language: [Python v{PYTHON_VERSION}](https://www.python.org/)

🧰 Framework: [Pyrogram v{PYROGRAM_VERSION}](https://github.com/pyrogram/pyrogram)

👨‍💻 Developer: [Anonymous](https://t.me/Ns_AnoNymouS)

📢 Channel: [NS Bots](https://t.me/NsBotsOfficial)

👥 Group: [Support Group](https://t.me/amcDevSupport)
"""


# command - description (follow this format while setting commands and use newline to set another command)
# command (``str``):  Text of the command; 1-32 characters. Can contain only lowercase English letters, digits and underscores.
# description (``str``) – Description of the command; 1-256 characters.
# Example:
# start - check whether bot alive or not
# about - check about me
      DEFAULT_COMMANDS = """ 
start - check whether bot alive or not
login - connect bot with your doodstream account
token - your api key to connect with doodstream 
myfiles - your doodstream account files
remote_actions - check remote uplaod status
status - check your account status
"""


# The message that should be sent when user press help button or send /help command
      HELP = """
**You need Help?? 😎**

✪ First use /login command and follow the steps given there.

✪ For uploading telegram files to your doodstream account forward me a tg file or video.

✪ For uploading links send me the link i will upload them using remote upload.

✪ For checking your files use command /myfiles.

✪ For checking active uploads use command /remote_actions.

✪ For checking your account status use command /status.
"""

# The message that should be sent when user send /login command
      LOGIN = """
--**Follow The below steps to login**--

    • Open [Dood stream](http://doodstream.com) and signin or singup to an account.

    • And then press the below button and search for API Key and copy the API Key and send here in the format `/token xxxxxxx...`

"""


# The message that should be sent immediatly after a command used
      PROCESSING = "**Processing....**"


# The message that should be sent when user press home button or sent /start command
# You can use some special Keyword specified below
#     BOT_FIRST: gives the bot first name
#     BOT_LAST: gives the bot last name
#     BOT_MENTION: gives the hyper link of bot with bot first name
#     USER_FIRST: gives the user first name
#     USER_LAST: gives the user last name
#     USER_MENTION: gives the hyper link of user with user first name
      START = """
Hi {USER_MENTION}

I am a doodstream bot to maintain your [doodstream](https://doodstream.com) account.

I can upload tg files to your doodstream account too. Check help button for more help.

**Maintained By:** [Anonymous](https://t.me/Ns_AnoNymouS)
"""