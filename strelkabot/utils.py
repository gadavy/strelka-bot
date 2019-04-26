import os
import json
import logging

import telegram


class ConfigManager():

    _CFG_FILE = "config.json"

    _cfg = dict()

    def __init__(self, config_file=None):
        if config_file:
            ConfigManager._CFG_FILE = config_file

            ConfigManager._read_cfg()

    @staticmethod
    def _read_cfg():
        if os.path.isfile(ConfigManager._CFG_FILE):
            with open(ConfigManager._CFG_FILE) as config_file:
                ConfigManager._cfg = json.load(config_file)
        else:
            cfg_file = ConfigManager._CFG_FILE
            exit(f"ERROR: No configuration file '{cfg_file}' found")

    @staticmethod
    def get(*keys):
        if not ConfigManager._cfg:
            ConfigManager._read_cfg()

        value = ConfigManager._cfg
        for key in keys:
            try:
                value = value[key]
            except KeyError as e:
                err = f"Couldn't read '{key}' from Config"
                logging.debug(f"{repr(e)} - {err}")
                return None

        return value if value is not None else None


class TelegramBotPlugin():

    def __init__(self, telegram_bot):
        self.tg = telegram_bot
        self.ADMIN_LIST = self._get_admin_list()

    @classmethod
    def send_typing(cls, func):
        """Decorator, sends typing action."""
        def wrapped(self, update, context, *args, **kwargs):
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=telegram.ChatAction.TYPING
            )
            return func(self, update, context, *args, **kwargs)
        return wrapped

    @classmethod
    def restricted(cls, func):
        """Decorator, restrict the access of a handler to only ADMIN_LIST"""
        def wrapped(self, update, context, *args, **kwargs):
            user_id = update.effective_user.id
            if user_id not in self.ADMIN_LIST:
                logging.info(
                    "Unauthorized access denied for {}.".format(user_id)
                )
                return
            return func(self, update, context, *args, **kwargs)
        return wrapped

    @classmethod
    def add_user(cls, func):
        """Decorator, add user to data base if he doesn't exist."""
        def wrapped(self, update, context, *args, **kwargs):
            if update.message:
                data = update.message.from_user
            elif update.inline_query:
                data = update.effective_user
            else:
                logging.warning("Can't save usage - {}".format(update))

            if self.tg.db.exists_user(data) is False:
                if self.tg.db.add_user(data) is not True:
                    logging.warning("Can't save user - {}".format(data.id))

            return func(self, update, context, *args, **kwargs)
        return wrapped

    # Read admins list from file.
    def _get_admin_list(self):

        path = "config/admin.json"

        try:
            if os.path.isfile(path):
                with open(path, 'r') as file:
                    return json.load(file)["admin_id"]
            else:
                exit(f"ERROR: No config file found at '{path}'")
        except KeyError as e:
            cls_name = f"Class: {type(self).__name__}"
            logging.error(f"{repr(e)} - {cls_name}")
            exit("ERROR: Can't read admin.json")
