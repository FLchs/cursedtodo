from configparser import ConfigParser
import os

xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or os.path.join(os.path.expanduser('~'), '.config')

Config = ConfigParser()
Config.read(os.path.join(xdg_config_home,"cursedtodo/config.ini"))
