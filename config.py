from __future__ import annotations

import json
from pathlib import Path


CONFIG_FILE = Path("config/config.json")


class Config:
    def __init__(self):
        self.reload()

    def reload(self):
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            self.data = json.load(f)

    @property
    def app(self):
        return self.data["app"]

    @property
    def database(self):
        return self.data["database"]

    @property
    def rss(self):
        return self.data["rss"]

    @property
    def lmstudio(self):
        return self.data["lmstudio"]

    @property
    def ai(self):
        return self.data["ai"]

    @property
    def ui(self):
        return self.data["ui"]

    @property
    def logging(self):
        return self.data["logging"]


config = Config()
