import os
import json
import logging


class ConfigManager:
    _CFG_FILE = "config.json"

    _cfg = dict()

    def __init__(self):
        ConfigManager._read_cfg()

    @staticmethod
    def _read_cfg():
        config_path = os.path.join(ConfigManager._CFG_FILE)
        if os.path.isfile(config_path):
            with open(config_path, 'r') as cofig_file:
                ConfigManager._cfg = json.load(cofig_file)
        else:
            cfg_file = ConfigManager._CFG_FILE
            exit("ERROR: No configuration file '{}' found".format(cfg_file))

    @staticmethod
    def get(*keys):
        if not ConfigManager._cfg:
            ConfigManager._read_cfg()

        value = ConfigManager._cfg
        for key in keys:
            try:
                value = value[key]
            except KeyError as e:
                err = "Couldn't read '{}' from Config".format(key)
                logging.debug("{} - {}".format(repr(e), err))
                return None

        return value if value is not None else None


ConfigManager().get("telegram")
