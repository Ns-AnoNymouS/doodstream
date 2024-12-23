from os import getenv

class Config:
    api_hash = getenv("API_HASH")
    api_id = int(getenv("API_ID", 12345))
    bot_token = getenv("BOT_TOKEN", "")
    database_url = getenv("DATABASE_URL", "")
    force_sub = getenv("FORCE_SUB", "")
    owner = list(int(user) for user in getenv("OWNER_ID", "1458029115").split(' '))
    support_group = getenv("SUPPORT_GROUP", "amcDevSupport").replace('@', '')
    updates_channel = getenv("UPDATES_CHANNEL", "NsBotsOfficial").replace('@', '')
