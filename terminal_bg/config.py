import configparser
import os

DEFAULT_CONFIG = {
    "Appearance": {
        "opacity": "0.8",
        "background_color": "rgba(0,0,0,0)"
    },
    "Behavior": {
        "default_command": "cava",
        "default_monitor": "0"
    }
}

CONFIG_PATH = os.path.expanduser("~/.config/terminal-bg/terminal-bg.conf")

def load_config():
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)

    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
    return config
