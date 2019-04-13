from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from telegrambot import TelegramBotPlugin


class Threshold(TelegramBotPlugin):

    START = 1

    def __init__(self, telegram_bot):
        self.tgb = telegram_bot
        self.tgb.dispatcher.add_handler(ConversationHandler(
            entry_points=[
                CallbackQueryHandler(self._start_cal, pattern="thr"),
                CommandHandler("set_threshold", self._start_com)
            ],

            states={self.START: [MessageHandler(Filters.text, self._input)]},

            fallbacks=[CallbackQueryHandler(self._escape, pattern="cancel")]
        ))

    @TelegramBotPlugin.send_typing
    def _start_cal(self, update, context):
        query = update.callback_query
        t_id = query.message.chat_id

        thr = self.tgb.data_base.get_user_thr(t_id)
        text = f"Порог оповещений: *{thr}* р. Введите целое число что бы изменить."
        keyboard = [[InlineKeyboardButton('Отмена ❌', callback_data='cancel')]]

        menu_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text, reply_markup=menu_markup, parse_mode=ParseMode.MARKDOWN
        )

        return self.START

    @TelegramBotPlugin.send_typing
    def _start_com(self, update, context):
        t_id = update.message.from_user.id

        thr = self.tgb.data_base.get_user_thr(t_id)
        text = f"Порог оповещений: *{thr}* р. Введите целое число что бы изменить."
        keyboard = [[InlineKeyboardButton('Отмена ❌', callback_data='cancel')]]

        menu_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            text, reply_markup=menu_markup, parse_mode=ParseMode.MARKDOWN
        )

        return self.START

    @TelegramBotPlugin.send_typing
    def _input(self, update, context):
        t_id = update.message.chat.id
        thr = update.message.text

        if thr.isdigit() is False:
            text = "*Используйте только цифры!*"
            keyboard = [
                [InlineKeyboardButton("Отмена ❌", callback_data="cancel")]
            ]
            menu_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                text, reply_markup=menu_markup, parse_mode=ParseMode.MARKDOWN
            )

            return self.START

        else:
            self.tgb.data_base.update_user_thr(t_id, thr)
            thr = self.tgb.data_base.get_user_thr(t_id)
            text = f"Новый порог - {thr} р."

            if self.tgb.data_base.get_user_ntf(t_id) is True:
                emoji = "🔔"
            else:
                emoji = "🔕"

            keyboard = [
                [InlineKeyboardButton(f"Оповещения {emoji}", callback_data="ntf")],
                [InlineKeyboardButton("Изменить порог", callback_data="thr")],
                [InlineKeyboardButton("Отмена ❌", callback_data="cancel")]
            ]
            menu_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(text, reply_markup=menu_markup)

            return ConversationHandler.END

    @TelegramBotPlugin.send_typing
    def _escape(self, update, context):
        query = update.callback_query
        t_id = query.message.chat_id

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
        query.edit_message_text(text, reply_markup=menu_markup)

        return ConversationHandler.END
