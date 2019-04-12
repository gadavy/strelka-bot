from telegram.ext import CallbackQueryHandler

from telegrambot import TelegramBotPlugin


class Cancel(TelegramBotPlugin):

    def __init__(self, telegram_bot):
        self.tgb = telegram_bot

        self.tgb.dispatcher.add_handler(CallbackQueryHandler(
            self._cbk_cancel, pattern="cancel"))

    def _cbk_cancel(self, update, context):
        query = update.callback_query
        context.bot.deleteMessage(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
