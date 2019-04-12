from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler

from telegrambot import TelegramBotPlugin


class Remove(TelegramBotPlugin):

    def __init__(self, telegram_bot):
        self.tgb = telegram_bot

        self.tgb.dispatcher.add_handler(MessageHandler(
            Filters.regex("УДАЛИТЬ КАРТУ 🗑"), self._msg_remove
        ))

        self.tgb.dispatcher.add_handler(CallbackQueryHandler(
            self._cbk_remove, pattern="str_del"))

    @TelegramBotPlugin.send_typing
    def _msg_remove(self, update, context):
        telegram_id = update.message.from_user.id
        cards = self.tgb.data_base.get_user_strelka(telegram_id)

        if len(cards) > 0:
            keyboard = list()
            for card in cards:
                keyboard.append(
                    [InlineKeyboardButton(
                        card,
                        callback_data="str_del{}".format(card)
                    )]
                )
            keyboard.append(
                [InlineKeyboardButton("Отмена ❌", callback_data="cancel")]
            )

            text = "Выберите карту для удаления:"
            menu_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(text, reply_markup=menu_markup)

        else:
            update.message.reply_text("У Вас нет привязанных карт.")

    @TelegramBotPlugin.send_typing
    def _cbk_remove(self, update, context):
        query = update.callback_query

        t_id = query.message.chat.id
        card = query.data[7::]

        if self.tgb.data_base.chek_user_strelka(t_id, card) is True:
            if self.tgb.data_base.remove_user_strelka(t_id, card) is True:
                query.edit_message_text("Карта № {} удалена.".format(card))
            else:
                query.edit_message_text("Возникла ошибка.")
        else:
            query.edit_message_text("Возникла ошибка.")
