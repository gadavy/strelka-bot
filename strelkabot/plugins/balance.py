from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from strelkabot.utils import TelegramBotPlugin


class Balance(TelegramBotPlugin):

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)

        self.tg.dispatcher.add_handler(MessageHandler(
            Filters.regex("УЗНАТЬ БАЛАНС 💰"), self._msg_balance
        ))

        self.tg.dispatcher.add_handler(CallbackQueryHandler(
            self._cbk_balance, pattern="b-"
        ))

    @run_async
    @TelegramBotPlugin.send_typing
    def _msg_balance(self, update, context):
        cards = self.tg.db.select_user_cards(update.message.from_user)

        if cards is None:
            msg = "‼ Возникла ошибка, попробуйте позже."
            update.message.reply_text(msg)

        elif len(cards) > 0:
            keyboard = list()

            for card in cards:
                callback = "b-{}".format(card)
                keyboard.append([InlineKeyboardButton(text=card,
                                                      callback_data=callback)])

            keyboard.append([InlineKeyboardButton(text="Отмена ❌",
                                                  callback_data="ex")])

            msg = "Выберите карту, баланс которой интересует: "
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(msg, reply_markup=markup)

        else:
            msg = "У Вас нет привязанных карт."
            update.message.reply_text(msg)

    @run_async
    def _cbk_balance(self, update, context):
        query = update.callback_query
        data = self.tg.db.select_user_balance(query.message.chat.id,
                                              query.data[2::])

        if data is None:
            msg = "‼ Возникла ошибка, попробуйте позже."
            query.edit_message_text(text=msg)

        else:
            txt = "{}, баланс карты _№{}_\nсоставляет: {} руб."
            msg = txt.format(data[1], data[2][-4::], data[3] // 100)
            query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)
