import os
import logging
import importlib

import telegram
from telegram.ext import Updater

from strelkabot.utils import ConfigManager as Cfg


class TelegramBot():

    def __init__(self, token, database):
        self.token = token
        self.db = database

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
            self.updater = Updater(self.token,
                                   request_kwargs=kwargs,
                                   use_context=True)

        except telegram.error.InvalidToken as ex:
            cls_name = f"Class: {type(self).__name__}"
            logging.error(f"{repr(ex)} - {cls_name}")
            exit("ERROR: Bot token not valid")

        except Exception as ex:
            cls_name = f"Class: {type(self).__name__}"
            logging.error(f"{repr(ex)} - {cls_name}")
            exit(f"ERROR: {ex}")

        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

        # Load classes in folder 'plugins'.
        self._load_plugins()

        # Add error handler.
        self.dispatcher.add_error_handler(self._tg_error)

    def bot_start_polling(self):
        """Start the bot."""
        self.updater.start_polling()

    def bot_idle(self):
        """Go in idle mode."""
        self.updater.idle()

    def _load_plugins(self):
        for _, _, files in os.walk("strelkabot/plugins"):
            files.sort()
            for file in files:
                if not file.lower().endswith(".py"):
                    continue
                if file.startswith("_"):
                    continue

                try:
                    module_name = file[:-3]
                    if module_name.startswith("*"):
                        class_name = module_name[1::].capitalize()
                    else:
                        class_name = module_name.capitalize()

                    module_path = f"strelkabot.plugins.{module_name}"
                    module = importlib.import_module(module_path)
                    plugin_class = getattr(module, class_name)
                    plugin_class(self)

                    msg = f"Plugin '{class_name}' from {module_path} loaded."
                    logging.info(msg)

                except Exception as ex:
                    msg = f"File '{file}' can't be loaded as a plugin: {ex}."
                    logging.warning(msg)

    # Handle all telegram and telegram.ext related errors.
    def _tg_error(self, update, context):
        logging.warning(
            "Update {}, caused error {}".format(update, context.error)
        )

        if not update:
            return

        error_msg = "‼ Telegram ERROR: *{}*".format(context.error)

        if update.message:
            update.message.reply_text(
                text=error_msg,
                parse_mode=telegram.ParseMode.MARKDOWN)

        elif update.callback_query:
            update.callback_query.message.reply_text(
                text=error_msg,
                parse_mode=telegram.ParseMode.MARKDOWN)
