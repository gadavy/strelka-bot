import logging
import requests

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

        if data is None or len(data) == 0:
            msg = self._request(query.data[2::])
            query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)

        else:
            txt = "Баланс карты _№{}_\nсоставляет: {} руб."
            msg = txt.format(data[0][2][-4::], data[0][3] / 100)
            query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)

    def _request(self, card):
        # region strelkakard params
        url = "https://strelkacard.ru/api/cards/status/"
        payload = {
            "cardnum": card,
            "cardtypeid": "3ae427a1-0f17-4524-acb1-a3f50090a8f3"}
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://strelkacard.ru/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)",
            "x-csrftoken": "null",
            "x-requested-with": "XMLHttpRequest"
        }
        # endregion
        try:
            r = requests.get(url, params=payload, headers=headers)
            balance = r.json()["balance"]

            txt = "Баланс карты _№{}_\nсоставляет: {} руб."
            msg = txt.format(card[-4::], balance / 100)

            return msg

        except Exception as ex:
            logging.warning("balance Error: '{}'".format(ex))
            msg = "‼ Возникла ошибка, попробуйте позже."

            return msg
