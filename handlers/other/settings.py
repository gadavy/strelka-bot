from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler

from telegrambot import TelegramBotPlugin


class Settings(TelegramBotPlugin):
    """Обработчик команды /start, /help."""
    def __init__(self, telegram_bot):
        self.tgb = telegram_bot

        self.tgb.dispatcher.add_handler(MessageHandler(
            Filters.regex("НАСТРОЙКИ ⚙"), self._inl_menu
        ))

        self.tgb.dispatcher.add_handler(CallbackQueryHandler(
            self._cbk_notification, pattern="ntf"))

    @TelegramBotPlugin.send_typing
    def _inl_menu(self, update, context):
        t_id = update.message.from_user.id
        if self.tgb.data_base.get_user_ntf(t_id) is True:
            emoji = "🔔"
        else:
            emoji = "🔕"

        text = "Настройки strelkabot."
        keyboard = [
            [InlineKeyboardButton(f"Оповещения {emoji}", callback_data="ntf")],
            [InlineKeyboardButton("Изменить порог", callback_data="thr")],
            [InlineKeyboardButton("Отмена ❌", callback_data="cancel")]
        ]
        menu_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text, reply_markup=menu_markup)

    @TelegramBotPlugin.send_typing
    def _cbk_notification(self, update, context):
        query = update.callback_query
        t_id = query.message.chat_id

        if self.tgb.data_base.get_user_ntf(t_id) is True:
            self.tgb.data_base.update_user_ntf(t_id, False)
        else:
            self.tgb.data_base.update_user_ntf(t_id, True)

        if self.tgb.data_base.get_user_ntf(t_id) is True:
            emoji = "🔔"
            text = "Оповещения  включены."
        else:
            emoji = "🔕"
            text = "Оповещения выключены."

        keyboard = [
            [InlineKeyboardButton(f"Оповещения {emoji}", callback_data="ntf")],
            [InlineKeyboardButton("Изменить порог", callback_data="thr")],
            [InlineKeyboardButton("Отмена ❌", callback_data="cancel")]
        ]
        menu_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text, reply_markup=menu_markup)
