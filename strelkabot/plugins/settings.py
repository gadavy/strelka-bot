from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from strelkabot.utils import TelegramBotPlugin


class Settings(TelegramBotPlugin):

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)

        self.tg.dispatcher.add_handler(MessageHandler(
            Filters.regex("НАСТРОЙКИ ⚙"), self._inl_menu
        ))

        self.tg.dispatcher.add_handler(CallbackQueryHandler(
            self._cbk_notification, pattern="ntf"))

    @run_async
    @TelegramBotPlugin.send_typing
    def _inl_menu(self, update, context):
        user_info = self.tg.db.select_user(update.message.from_user)

        if user_info is None:
            msg = "‼ Возникла ошибка, попробуйте позже."
            update.message.reply_text(msg)
            return

        else:
            emoji = "🔔" if user_info[6] == 1 else "🔕"

        keyboard = [
            [InlineKeyboardButton(f"Оповещения {emoji}", callback_data="ntf")],
            [InlineKeyboardButton("Изменить порог", callback_data="thr")],
            [InlineKeyboardButton("Отмена ❌", callback_data="ex")]
        ]

        msg = "Настройки strelkabot."
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(msg, reply_markup=markup)

    @run_async
    def _cbk_notification(self, update, context):
        query = update.callback_query
        user_info = self.tg.db.select_user(update.effective_user)

        if user_info is None:
            msg = "‼ Возникла ошибка, попробуйте позже."
            query.edit_message_text(msg)
            return

        elif user_info[6] == 1:
            data = update.effective_user.__dict__
            data["notification"] = 0
            data["threshold"] = user_info[7]

            if self.tg.db.update_user(data) is True:
                emoji = "🔕"
                msg = "Оповещения отключены."

            else:
                msg = "‼ Возникла ошибка, попробуйте позже."
                query.edit_message_text(msg)
                return

        else:
            data = update.effective_user.__dict__
            data["notification"] = 1
            data["threshold"] = user_info[7]
            self.tg.db.update_user(data)

            if self.tg.db.update_user(data) is True:
                emoji = "🔔"
                msg = "Оповещения включены."

            else:
                msg = "‼ Возникла ошибка, попробуйте позже."
                query.edit_message_text(msg)
                return

        keyboard = [
            [InlineKeyboardButton(f"Оповещения {emoji}", callback_data="ntf")],
            [InlineKeyboardButton("Изменить порог", callback_data="thr")],
            [InlineKeyboardButton("Готово ✅", callback_data="ex")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(msg, reply_markup=markup)
