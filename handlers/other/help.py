from telegram import ParseMode
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler

from telegrambot import TelegramBotPlugin


class Help(TelegramBotPlugin):
    """Обработчик команды /start, /help."""
    def __init__(self, telegram_bot):
        self.tgb = telegram_bot
        self.tgb.dispatcher.add_handler(CommandHandler("help", self._help))

        self.tgb.dispatcher.add_handler(MessageHandler(
            Filters.regex("ПОМОЩЬ ❓"), self._help
        ))

    @TelegramBotPlugin.send_typing
    def _help(self, update, context):
        text = "_Я могу..._"
        update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
