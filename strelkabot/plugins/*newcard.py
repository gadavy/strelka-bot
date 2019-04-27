import requests

from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from strelkabot.utils import TelegramBotPlugin


class Newcard(TelegramBotPlugin):

    START = 1

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)

        self.tg.dispatcher.add_handler(ConversationHandler(
            entry_points=[
                MessageHandler(Filters.regex("ДОБАВИТЬ КАРТУ 🆕"), self._start),
                CommandHandler("add_card", self._start)
            ],

            states={self.START: [MessageHandler(Filters.text, self._input)]},

            fallbacks=[CallbackQueryHandler(self._escape, pattern="ex")]
        ))

    @TelegramBotPlugin.send_typing
    @TelegramBotPlugin.insert_user
    def _start(self, update, context):
        keyboard = [[InlineKeyboardButton("Отмена ❌", callback_data="ex")]]

        msg = "Напишите номер карты цифрами без пробелов."
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(msg, reply_markup=markup)

        return self.START

    @TelegramBotPlugin.send_typing
    def _input(self, update, context):
        input_ = update.message.text

        # Check input on letters and characters.
        if input_.isdigit() is False:
            keyboard = [[InlineKeyboardButton("Отмена ❌", callback_data="ex")]]

            msg = "*Используйте только цифры!*"
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(msg,
                                      reply_markup=markup,
                                      parse_mode=ParseMode.MARKDOWN)

            return self.START

        else:
            msg = self._add_card(update.message.chat.id, input_)
            update.message.reply_text(msg)

            return ConversationHandler.END

    def _escape(self, update, context):
        msg = 'Добавление карты отменено.'
        context.bot.edit_message_text(
            text=msg,
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id
        )
        return ConversationHandler.END

    def _check_card(self, card):
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
            if r.status_code != 200:
                return r.reason

        except Exception as ex:
            return ex

        else:
            return True

    def _add_card(self, tg_id, card):
        # Check input on database user cards.
        request = self.tg.db.exists_user_card(tg_id, card)

        if request is True:
            msg = "Данная карта уже привязана к Вашему аккаунту."
            return msg

        elif request is False:

            if self._check_card(card) is True:
                # Check card validation.
                request = self.tg.db.exists_card(card)
                if request is True:
                    # Add link user/strelka to db.
                    if self.tg.db.insert_user_card(tg_id, card) is True:
                        msg = "Ваша карта успешно добавлена."
                        return msg

                    else:
                        msg = "‼ Возникла ошибка, попробуйте позже."
                        return msg

                elif request is False:
                    # Add card to db.
                    if self.tg.db.insert_card(card) is True:
                        # Add link user/strelka to db.
                        if self.tg.db.insert_user_card(tg_id, card) is True:
                            msg = "Ваша карта успешно добавлена."
                            return msg

                        else:
                            msg = "‼ Возникла ошибка, попробуйте позже."
                            return msg

                    else:
                        msg = "‼ Возникла ошибка, попробуйте позже."
                        return msg

                else:
                    msg = "‼ Возникла ошибка, попробуйте позже."
                    return msg

            else:
                msg = "Карты не существует, проверьте правильность ввода."
                return msg

        else:
            msg = "‼ Возникла ошибка, попробуйте позже."
            return msg
