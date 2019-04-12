import os
import logging
import importlib

from telegram import ChatAction
from telegram import ParseMode
from telegram.ext import Updater

from confmanager import ConfigManager as Cfg


class TelegramBot():
    """
    Подключает используемые ботом обработчики и инициирует бота командами
    bot_start_polling + bot_idle.

    Metods:
        bot_start_polling: запуск бота,
        bot_idle: поддерживает работу бота до нажатия Ctrl-C.

    """
    def __init__(self, bot_token, data_base):
        self.bot_token = bot_token
        self.data_base = data_base

        # Loading connection settings from config.json.
        proxy_url = Cfg.get("telegram", "proxy_url")
        read_timeout = Cfg.get("telegram", "read_timeout")
        connect_timeout = Cfg.get("telegram", "connect_timeout")
        con_pool_size = Cfg.get("telegram", "con_pool_size")

        kwargs = dict()
        if proxy_url:
            kwargs["proxy_url"] = proxy_url
        if read_timeout:
            kwargs["read_timeout"] = read_timeout
        if connect_timeout:
            kwargs["connect_timeout"] = connect_timeout
        if con_pool_size:
            kwargs["con_pool_size"] = con_pool_size

        try:
            self.updater = Updater(bot_token,
                                   request_kwargs=kwargs,
                                   use_context=True)
        except Exception:
            exit("ERROR: Bot token or kwargs not valid")

        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

        # Add bot handlers.
        self._load_handlers("conversation")
        self._load_handlers("other")

        # Add error handler.
        self.dispatcher.add_error_handler(self._tg_error)

    def bot_start_polling(self):
        """Start bot."""
        self.updater.start_polling()

    def bot_idle(self):
        """Run the bot until you press Ctrl-C."""
        self.updater.idle()

    def _tg_error(self, update, context):
        """Log and send Errors caused by Updates."""
        logging.warning(
            "Update {}, caused error {}".format(update, context.error)
        )

        if not update:
            return

        error_msg = "‼ Telegram ERROR: *{}*".format(context.error)

        if update.message:
            update.message.reply_text(
                text=error_msg,
                parse_mode=ParseMode.MARKDOWN)
        elif update.callback_query:
            update.callback_query.message.reply_text(
                text=error_msg,
                parse_mode=ParseMode.MARKDOWN)

    def _load_handlers(self, folder):
        """Load hendlers for bot."""
        path = os.path.join("handlers", folder)
        for _, _, files in os.walk(path):
            for file_ in files:
                if not file_.lower().endswith(".py"):
                    continue
                if file_.startswith("_"):
                    continue

                try:
                    module_name = file_[:-3]
                    module_path = "handlers.{}.{}".format(folder, module_name)
                    module = importlib.import_module(module_path)
                    plugin_class = getattr(module, module_name.capitalize())
                    plugin_class(self)
                    msg = f"Plugin {module_name} from {module_path} loaded."
                    logging.info(msg)

                except Exception as ex:
                    msg = f"File '{file_}' can't be loaded as a plugin: {ex}."
                    logging.warning(msg)


class TelegramBotPlugin():
    """Plugins for telegram bot."""
    def __init__(self, telegram_bot):
        self.tgb = telegram_bot

    @classmethod
    def send_typing(cls, func):
        """Sends typing action while processing func command."""
        def _send_typing_action(self, update, context, *args, **kwargs):
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=ChatAction.TYPING
            )
            return func(self, update, context, *args, **kwargs)
        return _send_typing_action

    @classmethod
    def add_user(cls, func):
        """Add user to data base."""
        def _add_user(self, update, context, *args, **kwargs):
            if update.message:
                data = update.message.from_user
            elif update.inline_query:
                data = update.effective_user
            else:
                logging.warning("Can't save usage - {}".format(update))
                return func(self, update, context, *args, **kwargs)

            if self.tgb.data_base.check_user(data.id) is False:
                if self.tgb.data_base.add_user(data) is not True:
                    logging.warning("Can't save usage - {}".format(update))

            return func(self, update, context, *args, **kwargs)
        return _add_user
