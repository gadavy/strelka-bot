from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from strelkabot.utils import TelegramBotPlugin


class Threshold(TelegramBotPlugin):

    START = 1

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)

        self.tg.dispatcher.add_handler(ConversationHandler(
            entry_points=[
                CallbackQueryHandler(self._start_cal, pattern="thr"),
                CommandHandler("set_threshold", self._start_com)
            ],

            states={self.START: [MessageHandler(Filters.text, self._input)]},

            fallbacks=[CallbackQueryHandler(self._escape, pattern="ex")]
        ))

    @TelegramBotPlugin.send_typing
    def _start_cal(self, update, context):
        query = update.callback_query
        user_info = self.tg.db.select_user(update.effective_user)

        if user_info is None:
            msg = "‼ Возникла ошибка, попробуйте позже."
            update.message.reply_text(msg)

            return

        else:
            thr = user_info[7] // 100
            msg = f"Threshold: *{thr}* р. Введите целое число для изменения."
            keyboard = [[InlineKeyboardButton('Отмена ❌', callback_data='ex')]]
            markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text=msg,
                                    reply_markup=markup,
                                    parse_mode=ParseMode.MARKDOWN)

            return self.START

    @TelegramBotPlugin.send_typing
    def _start_com(self, update, context):
        user_info = self.tg.db.select_user(update.message.from_user)

        if user_info is None:
            msg = "‼ Возникла ошибка, попробуйте позже."
            update.message.reply_text(msg)

            return

        else:
            thr = user_info[7] // 100
            msg = f"Threshold: *{thr}* р. Введите целое число для изменения."
            keyboard = [[InlineKeyboardButton('Отмена ❌', callback_data='ex')]]
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(text=msg,
                                      reply_markup=markup,
                                      parse_mode=ParseMode.MARKDOWN)

            return self.START

    @TelegramBotPlugin.send_typing
    def _input(self, update, context):
        user_info = self.tg.db.select_user(update.message.from_user)
        input_ = update.message.text

        if user_info is None:
            msg = "‼ Возникла ошибка, попробуйте позже."
            update.message.reply_text(msg)

            return ConversationHandler.END

        elif input_.isdigit() is False:
            keyboard = [[InlineKeyboardButton("Отмена ❌", callback_data="ex")]]

            msg = "*Используйте только цифры!*"
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(msg,
                                      reply_markup=markup,
                                      parse_mode=ParseMode.MARKDOWN)

            return self.START

        else:
            data = update.effective_user.__dict__
            data["notification"] = user_info[6]
            data["threshold"] = int(input_) * 100

            if self.tg.db.update_user(data) is not True:
                msg = "‼ Возникла ошибка, попробуйте позже."
                update.message.reply_text(msg)

                return ConversationHandler.END

            else:
                emoji = "🔔" if user_info[6] == 1 else "🔕"

            keyboard = [
                [InlineKeyboardButton(f"Оповещения {emoji}", callback_data="ntf")],
                [InlineKeyboardButton("Изменить порог", callback_data="thr")],
                [InlineKeyboardButton("Готово ✅", callback_data="ex")]
            ]

            msg = f"Минимальный баланс изменен и составляет - {input_} р."
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(text=msg, reply_markup=markup)

            return ConversationHandler.END

    @TelegramBotPlugin.send_typing
    def _escape(self, update, context):
        user_info = self.tg.db.select_user(update.message.from_user)
        query = update.callback_query

        if user_info is None:
            msg = "‼ Возникла ошибка, попробуйте позже."
            query.edit_message_text(msg)

            return ConversationHandler.END

        else:
            emoji = "🔔" if user_info[6] == 1 else "🔕"

        keyboard = [
            [InlineKeyboardButton(f"Оповещения {emoji}", callback_data="ntf")],
            [InlineKeyboardButton("Изменить порог", callback_data="thr")],
            [InlineKeyboardButton("Готово ✅", callback_data="ex")]
        ]

        msg = "Настройки."
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=msg, reply_markup=markup)

        return ConversationHandler.END
