import requests

from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from telegrambot import TelegramBotPlugin


class Newcard(TelegramBotPlugin):

    START = 1

    def __init__(self, telegram_bot):
        self.tgb = telegram_bot
        self.tgb.dispatcher.add_handler(ConversationHandler(
                entry_points=[
                    MessageHandler(Filters.regex(
                        "ДОБАВИТЬ КАРТУ 🆕"), self._start
                    )
                ],
                states={
                    self.START: [
                        MessageHandler(Filters.text, self._input),
                        ]
                },
                fallbacks=[
                    CallbackQueryHandler(self._escape, pattern="cancel")
                ]
            )
        )

    @TelegramBotPlugin.send_typing
    @TelegramBotPlugin.add_user
    def _start(self, update, context):
        text = "Напишите номер карты цифрами без пробелов."
        keyboard = [
            [InlineKeyboardButton("Отмена ❌", callback_data="cancel")]
        ]
        menu_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text, reply_markup=menu_markup)
        return self.START

    @TelegramBotPlugin.send_typing
    def _input(self, update, context):
        t_id = update.message.from_user.id
        card = update.message.text

        # Проверка на наличие других символов кроме цифр.
        if card.isdigit() is False:
            text = "*Используйте только цифры!*"
            keyboard = [
                [InlineKeyboardButton("Отмена ❌", callback_data="cancel")]
            ]
            menu_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                text, reply_markup=menu_markup, parse_mode=ParseMode.MARKDOWN
            )
            return self.START

        # Проверка на наличие карты в привязанных картах.
        elif card in self.tgb.data_base.get_user_strelka(t_id):
            text = "Данная карта уже привязана к Вашему аккаунту."
            update.message.reply_text(text)
            return ConversationHandler.END

        # Проверка валидности карты через сайт.
        elif self._check_card(card) is True:
            # Проверка существования карты в таблица 'cards_strelka'.
            if self.tgb.data_base.check_strelka(card) is False:
                self.tgb.data_base.add_strelka(card)
                self.tgb.data_base.add_user_strelka(t_id, card)
                if self.tgb.data_base.chek_user_strelka(t_id, card) is True:
                    update.message.reply_text("Карта успешно добавлена.")
                    return ConversationHandler.END
                else:
                    update.message.reply_text("Возникла ошибка :с.")
                    return ConversationHandler.END
            else:
                self.tgb.data_base.add_user_strelka(t_id, card)
                if self.tgb.data_base.chek_user_strelka(t_id, card) is True:
                    update.message.reply_text("Карта успешно добавлена.")
                    return ConversationHandler.END
                else:
                    update.message.reply_text("Возникла ошибка :с.")
                    return ConversationHandler.END

        else:
            update.message.reply_text("Некорректные данные.")
            return ConversationHandler.END

    def _escape(self, update, context):
        query = update.callback_query
        text = 'Добавление карты отменено.'
        context.bot.edit_message_text(
            text=text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
        return ConversationHandler.END

    def _check_card(self, card):
        # Проверка карты через сайт, если она существует, возвращает True.
        try:
            CARD_TYPE_ID = '3ae427a1-0f17-4524-acb1-a3f50090a8f3'
            payload = {'cardnum': card, 'cardtypeid': CARD_TYPE_ID}
            r = requests.get('http://strelkacard.ru/api/cards/status/',
                             params=payload)
            if r.status_code != 200:
                return r.reason
        except Exception as error:
            return error
        return True
