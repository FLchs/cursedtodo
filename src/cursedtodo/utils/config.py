from configparser import ConfigParser
import os
from argparse import ArgumentParser

# TODO: this does not spark joy

xdg_config_home = os.environ.get("XDG_CONFIG_HOME") or os.path.join(
    os.path.expanduser("~"), ".config"
)
default_config_path = os.path.join(xdg_config_home, "cursedtodo/config.ini")

parser = ArgumentParser(description="Your program description")
parser.add_argument("-c", "--config", help="Config file path")
config_file = parser.parse_args().config or default_config_path


Config = ConfigParser()
Config.read(config_file)
