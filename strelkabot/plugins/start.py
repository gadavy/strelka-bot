from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async

from strelkabot.utils import TelegramBotPlugin


class Start(TelegramBotPlugin):

    START_FILE = "res/start.md"

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)
        self.tg.dispatcher.add_handler(CommandHandler("start", self._start))

    @run_async
    @TelegramBotPlugin.send_typing
    @TelegramBotPlugin.insert_user
    def _start(self, update, context):
        with open(self.START_FILE, "r", encoding="utf8") as file:
            content = file.readlines()

        keyboard = [
            [KeyboardButton("УЗНАТЬ БАЛАНС 💰")],
            [KeyboardButton("ДОБАВИТЬ КАРТУ 🆕")],
            [KeyboardButton("УДАЛИТЬ КАРТУ 🗑")],
            [KeyboardButton("НАСТРОЙКИ ⚙"), KeyboardButton("ПОМОЩЬ ❓")]
        ]

        menu_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,)
        update.message.reply_text("".join(content), reply_markup=menu_markup)
