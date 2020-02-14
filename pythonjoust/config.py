import configparser
import logging
import os

game_root = os.getcwd()
config_file_path = os.path.join(game_root, 'config.ini')


def parse_bool(value):
    if value:
        if value is True:
            return True
        elif value.lower() in ("true", "yes"):
            return True
    return False


class OptionField(object):
    def __init__(self, name, default, option_type):
        self.name = name
        self.default = default
        self.option_type = option_type


class ConfigurableOptions(object):
    fields = ()

    def __init__(self, **options):
        for field in self.fields:
            value = options.get(field.name, field.default)
            setattr(self, field.name, field.option_type(value))

    def export(self):
        return {
            field.name: getattr(self, field.name, field.default)
            for field in self.fields
        }


class GameOptions(ConfigurableOptions):
    fields = (
        OptionField('use_alt_sprites', False, parse_bool),
    )


def load_ini():
    parser = configparser.ConfigParser()
    try:
        parser.read(config_file_path)
        options = GameOptions(**parser['options'])
    except (IOError, KeyError):
        logging.warning("Could not read config file, writing the default one")
        options = GameOptions()
        save_ini(options)

    return options


def save_ini(options):
    parser = configparser.ConfigParser()
    try:
        new_opts = {
            'options': options.export(),
        }
        parser.update(new_opts)
        with open(config_file_path, 'w') as file_:
            parser.write(file_)
    except IOError:
        logging.error("Could not write config file.")
