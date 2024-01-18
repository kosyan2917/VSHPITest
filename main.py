import os.path
import random
from typing import List
import undetected_chromedriver
import requests
import lxml
import urllib.request
from bs4 import BeautifulSoup
import asyncio
from importlib import import_module

import plugin


class ImageParser:

    def __init__(self):
        self.plugins = self.load_plugins()

    def get_data(self, tags: List[str], amount: int = 10):
        self.plugins[0].parse(tags, amount)

    @staticmethod
    def load_plugins():
        loaded_plugins = []
        plugs = os.listdir('plugins')
        for plug in plugs:
            if plug.endswith('.py'):
                import_module('plugins.' + plug[:-3])
        for plug in plugin.Plugin.__subclasses__():
            loaded_plugins.append(plug())
        return loaded_plugins


if __name__ == '__main__':
    parser = ImageParser()
    print(parser.plugins)
    # parser.get_data(['cat', 'dog'], 1000)