import json
from pathlib import Path


class Configurator:
    def __init__(self):
        self._config = {}

    def load_from_json(self, path):
        with Path(path).open(encoding="utf-8") as f:
            self._config = json.load(f)

    def __getitem__(self, key):
        return self._config[key]

    def get(self, key, default=None):
        return self._config.get(key, default)


config = Configurator()
