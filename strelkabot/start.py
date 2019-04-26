import os
import json
import logging
import logging.handlers
from argparse import ArgumentParser

from strelkabot.utils import ConfigManager as Cfg
from strelkabot.database import Database
from strelkabot.telegrambot import TelegramBot


class StrelkaTelegramBot():

    def __init__(self):
        # Parse command line arguments.
        self.args = self._parse_args()

        # Load config file.
        self.Cfg = Cfg(self.args.config)

        # Set up logging.
        log_path = self.args.logfile
        log_level = self.args.loglevel
        self._init_logger(log_path, log_level)

        # Create database.
        self.database = Database()

        # Create bot.
        bot_token = self._get_bot_token()
        self.telegram_bot = TelegramBot(bot_token, self.database)

    # Parse arguments.
    def _parse_args(self):
        desc = "Telegram bot for strelkacard."
        parser = ArgumentParser(description=desc)

        # Config file path
        parser.add_argument(
            "-cfg",
            dest="config",
            help="path to conf file",
            default="config/config.json",
            required=False,
            metavar="FILE")

        # Save logfile.
        parser.add_argument(
            "--no-logfile",
            dest="savelog",
            action="store_false",
            help="don't save logs to file",
            required=False)
        parser.set_defaults(savelog=True)

        # Logfile path.
        parser.add_argument(
            "-log",
            dest="logfile",
            help="path to logfile",
            default="log/strelkacard.log",
            required=False,
            metavar="FILE")

        # Log level.
        parser.add_argument(
            "-lvl",
            dest="loglevel",
            type=int,
            choices=[0, 10, 20, 30, 40, 50],
            help="Disabled, Debug, Info, Warning, Error, Critical",
            default=20,
            required=False)

        # Bot token.
        parser.add_argument(
            "-tkn",
            dest="token",
            help="Telegram bot token",
            required=False,
            default=None)

        return parser.parse_args()

    def _init_logger(self, logfile, level):
        logger = logging.getLogger()
        logger.setLevel(level)

        log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

        # Log to console.
        console_log = logging.StreamHandler()
        console_log.setFormatter(logging.Formatter(log_format))
        console_log.setLevel(level)

        logger.addHandler(console_log)

        # Save logs if enabled.
        if self.args.savelog:
            # Create 'log' directory if not present
            log_path = os.path.dirname(logfile)
            if not os.path.exists(log_path):
                os.makedirs(log_path)

            file_log = logging.handlers.TimedRotatingFileHandler(
                logfile,
                when="D",
                encoding="utf-8")

            file_log.setFormatter(logging.Formatter(log_format))
            file_log.setLevel(level)

            logger.addHandler(file_log)

    # Read bot token from file.
    def _get_bot_token(self):
        if self.args.token:
            return self.args.token

        token_path = "config/token.json"

        try:
            if os.path.isfile(token_path):
                with open(token_path, 'r') as file:
                    return json.load(file)["telegram"]
            else:
                exit(f"ERROR: No token file found at '{token_path}'")
        except KeyError as e:
            cls_name = f"Class: {type(self).__name__}"
            logging.error(f"{repr(e)} - {cls_name}")
            exit("ERROR: Can't read bot token")

    def start(self):
        self.telegram_bot.bot_start_polling()
        self.telegram_bot.bot_idle()
