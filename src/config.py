"""
Config operations.
"""

import os
from pathlib import Path
import json


HOME = Path(os.environ['HOME'])
DEFAULT_JOURNAL_FILE = HOME / ".myjournal.txt"

EMPTY_CONFIG = {
    'journal_file': str(DEFAULT_JOURNAL_FILE),
    'dateformat': '%d-%m-%Y',
}

CONFIG_PATH = HOME / '.config/livinglogs'
CONFIG_FILE = CONFIG_PATH / 'config.json'

if not os.path.exists(CONFIG_PATH):
    # Create config folder if it doesn't exist.
    os.mkdir(CONFIG_PATH)


class ConfigError(Exception):
    pass

class Config:
    def __init__(self, file=CONFIG_FILE):
        self.file = file
        self.config = {}

        if not os.path.exists(self.file):
            self._generate_config()
            self.config = EMPTY_CONFIG
        else:
            # Load config
            self._load_config()

    def _generate_config(self):
        """Generate a new config with default values."""

        with open(self.file, 'w') as file:
            json.dump(EMPTY_CONFIG, file)

    def _load_config(self):
        with open(self.file, 'r') as file:
            try:
                self.config = json.load(file)
            except json.JSONDecodeError:
                raise ConfigError("Couldn't load config.")

    def save(self):
        """Saves self.config to the config file."""

        with open(self.file, 'w') as file:
            json.dump(self.config, file)

