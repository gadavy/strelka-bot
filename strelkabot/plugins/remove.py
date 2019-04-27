from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from strelkabot.utils import TelegramBotPlugin


class Remove(TelegramBotPlugin):

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)

        self.tg.dispatcher.add_handler(MessageHandler(
            Filters.regex("УДАЛИТЬ КАРТУ 🗑"), self._msg_remove
        ))

        self.tg.dispatcher.add_handler(CallbackQueryHandler(
            self._cbk_remove, pattern="d-"))

    @run_async
    @TelegramBotPlugin.send_typing
    def _msg_remove(self, update, context):
        cards = self.tg.db.select_user_cards(update.message.from_user)

        if cards is None:
            msg = "‼ Возникла ошибка, попробуйте позже."
            update.message.reply_text(msg)

        elif len(cards) > 0:
            keyboard = list()

            for card in cards:
                callback = "d-{}".format(card)
                keyboard.append([InlineKeyboardButton(text=card,
                                                      callback_data=callback)])

            keyboard.append([InlineKeyboardButton(text="Отмена ❌",
                                                  callback_data="ex")])

            msg = "Выберите карту для удаления: "
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(msg, reply_markup=markup)

        else:
            msg = "У Вас нет привязанных карт."
            update.message.reply_text(msg)

    @run_async
    def _cbk_remove(self, update, context):
        query = update.callback_query
        card = query.data[2::]

        if self.tg.db.delete_user_card(query.message.chat.id, card) is True:
            msg = "Карта № {} успешно удалена.".format(card)
            query.edit_message_text(msg)

        else:
            msg = "‼ Возникла ошибка, попробуйте позже"
            query.edit_message_text(msg)
