from telegram import ParseMode
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler

from telegrambot import TelegramBotPlugin


class Help(TelegramBotPlugin):
    """Обработчик команды /start, /help."""
    def __init__(self, telegram_bot):
        self.tgb = telegram_bot
        self.tgb.dispatcher.add_handler(CommandHandler("help", self._help))

        self.tgb.dispatcher.add_handler(MessageHandler(
            Filters.regex("ПОМОЩЬ ❓"), self._help
        ))

    @TelegramBotPlugin.send_typing
    def _help(self, update, context):
        text = (
            "• Привязать новую карту можно нажав кнопку <b>'добавить карту'"
            "</b> или командой /add_card;\n\n• Для получения текущего баланса"
            " карты стрелка, нажмите <b>'узнать баланс'</b> и в появившемся "
            "меню выберите интересующую Вас карту.\n\n• Для удаления карты -"
            " нажмите <b>'удалить карту'</b> и в появившемся меню выберите "
            "интересующую Вас карту\n\n• Для отключения уведомлений перейдите"
            " в настройки и нажмите <b>'оповещения'</b>.\n\n• Для изменения "
            "порога оповещений нажмите кнопку <b>'изменить порог'</b> в меню "
            "настроек или используйте команду /set_threshold."
        )

        update.message.reply_text(text, parse_mode=ParseMode.HTML)
