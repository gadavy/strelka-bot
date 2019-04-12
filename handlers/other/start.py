from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler

from telegrambot import TelegramBotPlugin


class Start(TelegramBotPlugin):
    """Обработчик команды /start, /help."""
    def __init__(self, telegram_bot):
        self.tgb = telegram_bot
        self.tgb.dispatcher.add_handler(CommandHandler("start", self._start))

    @TelegramBotPlugin.send_typing
    @TelegramBotPlugin.add_user
    def _start(self, update, context):
        text = "Добро пожаловать!"
        keyboard = [
            [KeyboardButton("УЗНАТЬ БАЛАНС 💰")],
            [KeyboardButton("ДОБАВИТЬ КАРТУ 🆕")],
            [KeyboardButton("УДАЛИТЬ КАРТУ 🗑")],
            [KeyboardButton("НАСТРОЙКИ ⚙"), KeyboardButton("ПОМОЩЬ ❓")]
        ]
        menu_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,)
        update.message.reply_text(text, reply_markup=menu_markup)
