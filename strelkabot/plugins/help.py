from telegram import ParseMode
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async

from strelkabot.utils import TelegramBotPlugin


class Help(TelegramBotPlugin):

    HELP_FILE = "res/help.md"

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)

        self.tg.dispatcher.add_handler(CommandHandler("help", self._help))

        self.tg.dispatcher.add_handler(MessageHandler(
            Filters.regex("ПОМОЩЬ ❓"), self._help
        ))

    @run_async
    @TelegramBotPlugin.send_typing
    def _help(self, update, context):
        with open(self.HELP_FILE, "r", encoding="utf8") as file:
            content = file.readlines()

        update.message.reply_text("".join(content), parse_mode=ParseMode.HTML)
