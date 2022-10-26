from pyrogram import Client
from pyrogram.types import BotCommand
from pyrogram.errors import BotCommandDescriptionInvalid


class Commands:
    def __init__(self, client: Client):
        self.client = client


    async def set_commands(self, str_commands: str):
        bot_commands, status = [], False
        for command in str_commands.splitlines():
            bot_command, description = (x.strip() for x in command.split('-'))
            bot_commands.append(BotCommand(bot_command[:32].lower(), description[:256]))
        try:
            status = await self.client.set_bot_commands(bot_commands)
            if status:
                text = "Sucessfully updated your bot commands.\n\n"
                text += "Please go back and open the bot again if you are not able to see the changes"
            else:
                text = "Unable to set the bot commands."
        except BotCommandDescriptionInvalid as e:
            text = "The command description was empty, too long or had invalid characters"
        except Exception as e:
            if 'BOT_COMMAND_INVALID' in e:
                text = "The command takes only lower english letter, underscores and digits"
            else:
                text = f"**Unkown Error:**\n\n{e}"
        return status, text