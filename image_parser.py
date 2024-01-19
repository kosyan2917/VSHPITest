import os.path
from typing import List, Type
from importlib import import_module
import numpy as np
import plugin


class ImageParser:

    def __init__(self, input_data: dict[str: dict[str: int]]):
        self.input_data = input_data

    def get_data(self) -> dict[str: int]:
        plugins = self.load_plugins()
        print(plugins)
        parse_data = {}
        for tag in self.input_data:
            parse_data[tag] = (self.input_data[tag]['train'] + self.input_data[tag]['test']) // len(plugins)
        # plugins[1].parse(parse_data)
        for plug in plugins:
            print(plug.parse(parse_data))

    def load_data(self) -> Type[np.array]:
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
