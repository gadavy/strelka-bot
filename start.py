import os
import logging
import logging.handlers

from database import DataBase
from telegrambot import TelegramBot
from confmanager import ConfigManager as Cfg


class StrelkaTelegramBot():

    def __init__(self):
        # Add logging.
        log_path = Cfg.get("settings", "log_path")
        log_level = Cfg.get("settings", "log_lvl")
        self._init_logger(log_path, log_level)

        # Add DataBase.
        self.data_base = DataBase()

        # Add telegram bot.
        bot_token = Cfg.get("telegram", "token")
        self.tgb = TelegramBot(bot_token, self.data_base)

    def _init_logger(self, logfile, level):
        logger = logging.getLogger()
        logger.setLevel(level)

        log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

        # Log to console.
        console_log = logging.StreamHandler()
        console_log.setFormatter(logging.Formatter(log_format))
        console_log.setLevel(level)

        logger.addHandler(console_log)

        # Log to file.
        log_path = os.path.dirname(logfile)
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        file_log = logging.handlers.TimedRotatingFileHandler(
            logfile,
            when="h",
            interval=12,
            encoding="utf-8"
        )

        file_log.setFormatter(logging.Formatter(log_format))
        file_log.setLevel(level)

        logger.addHandler(file_log)

    def start(self):
        self.tgb.bot_start_polling()
        self.tgb.bot_idle()
