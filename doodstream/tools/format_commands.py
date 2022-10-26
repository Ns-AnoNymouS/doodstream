from pyrogram import Client
from pyrogram.errors import BotCommandInvalid


class Commands:
    def __init__(self):
        self.client = Client


    async def set_commands(self, str_commands: str):
        bot_commands = []
        for command in commands.splitlines():
            bot_command, description = (x.strip() for x in command.split('-'))
            bot_commands.append(BotCommand(bot_command.lower(), description))
        try:
            sts = await self.client.set_bot_commands(bot_commands)
            if sts:
                txt = "Sucessfully updated your bot commands.\n\n"
                txt += "Please go back and open the bot again if you are not able to see the changes"
            else:
                txt = "Unable to set the bot commands."
        except BotCommandInvalid:
            txt = "The command contains some invalid characters"
        except Exception as e:
            txt = f"**Unkown Error:**\n\n{e}"
        return txt