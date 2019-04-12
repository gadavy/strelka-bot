import requests

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler

from telegrambot import TelegramBotPlugin


class Balance(TelegramBotPlugin):

    def __init__(self, telegram_bot):
        self.tgb = telegram_bot

        self.tgb.dispatcher.add_handler(MessageHandler(
            Filters.regex("УЗНАТЬ БАЛАНС 💰"), self._msg_balance
        ))

        self.tgb.dispatcher.add_handler(CallbackQueryHandler(
            self._cbk_balance, pattern="str_bal"))

    @TelegramBotPlugin.send_typing
    def _msg_balance(self, update, context):
        telegram_id = update.message.from_user.id
        cards = self.tgb.data_base.get_user_strelka(telegram_id)

        if len(cards) > 0:
            keyboard = list()
            for card in cards:
                keyboard.append(
                    [InlineKeyboardButton(
                        card,
                        callback_data="str_bal{}".format(card)
                    )]
                )
            keyboard.append(
                [InlineKeyboardButton("Отмена ❌", callback_data="cancel")]
            )

            text = "Выберите карту, баланс которой интересует:"
            menu_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(text, reply_markup=menu_markup)

        else:
            update.message.reply_text("У Вас нет привязанных карт.")

    @TelegramBotPlugin.send_typing
    def _cbk_balance(self, update, context):
        query = update.callback_query
        card = query.data[7::]

        CARD_TYPE_ID = "3ae427a1-0f17-4524-acb1-a3f50090a8f3"
        payload = {"cardnum": card, "cardtypeid": CARD_TYPE_ID}

        try:
            r = requests.get("http://strelkacard.ru/api/cards/status/",
                             params=payload)
            balance = r.json()
            result = balance["balance"] / 100

        except Exception as ex:
            text = "Возникла ошибка:\n{}".format(ex)

        else:
            text = "Баланс карты\n№ {}\nсоставляет: {} руб.".format(card,
                                                                    result)

        finally:
            query.edit_message_text(text=text)
