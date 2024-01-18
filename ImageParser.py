import os.path
import random
from typing import List
import requests
import lxml
import urllib.request
from bs4 import BeautifulSoup
import asyncio
from importlib import import_module

import plugin


class ImageParser:

    def get_data(self, input_data: dict[str: int]) -> None:
        plugins = self.load_plugins()
        # for tag in input_data:
        #     input_data[tag] = input_data[tag] // len(plugins)
        # for plug in plugins:
        #     plug.parse(input_data)
        plugins[1].parse(input_data)

    def load_data(self) -> List[List[int]]:
        pass

    @staticmethod
    def load_plugins() -> List[plugin.Plugin]:
        loaded_plugins = []
        plugs = os.listdir('plugins')
        for plug in plugs:
            if plug.endswith('.py'):
                import_module('plugins.' + plug[:-3])
        for plug in plugin.Plugin.__subclasses__():
            loaded_plugins.append(plug())
        return loaded_plugins


ImageParser.load_plugins()
