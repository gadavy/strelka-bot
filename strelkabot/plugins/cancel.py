from telegram.ext import CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from strelkabot.utils import TelegramBotPlugin


class Cancel(TelegramBotPlugin):

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)

        self.tg.dispatcher.add_handler(CallbackQueryHandler(
            self._cbk_cancel, pattern="ex"))

    @run_async
    def _cbk_cancel(self, update, context):
        query = update.callback_query

        context.bot.deleteMessage(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id)
