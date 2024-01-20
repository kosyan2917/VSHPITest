import os.path
from typing import List, Type
from importlib import import_module
import numpy as np
import plugin
from PIL import Image, ImageFile

class ImageParser:

    def __init__(self, input_data: dict[str: dict[str: int]]):
        self.input_data = input_data
        ImageFile.LOAD_TRUNCATED_IMAGES = True
    def get_data(self) -> dict[str: int]:
        plugins = self.load_plugins()
        print(plugins)
        parse_data = {}
        for tag in self.input_data:
            parse_data[tag] = (self.input_data[tag]['train'] + self.input_data[tag]['test']) // len(plugins)
        # plugins[1].parse(parse_data)
        for plug in plugins:
            print(plug.parse(parse_data))

    def load_data(self, max_height: int = 500, crop_width: int = None) -> (np.array, np.array, np.array, np.array):
        if crop_width is None:
            crop_width = max_height * 1.5
        train_data = []
        train_tags = []
        test_data = []
        test_tags = []
        train_counter = 0
        counter_tag = 0
        max_width = 0
        for tag in self.input_data:
            if not os.path.exists(tag):
                raise FileNotFoundError(f"Папка с тегом {tag} не найдена. Возможно, вы не скачали картинки по тегу {tag}")
            wanted_amount = self.input_data[tag]['train'] + self.input_data[tag]['test']
            actual_amount = len(os.listdir(tag))
            train_amount = self.input_data[tag]['train']
            test_amount = self.input_data[tag]['test']
            if actual_amount < wanted_amount:
                print(f"В папке с тегом {tag} находится {actual_amount} картинок, пр"
                      f"и запрошенном количестве {wanted_amount}. Данные для x_train и x_test будут "
                      f"собраны из {actual_amount} картинок пропорционально заданному количеству.")
                train_amount = int(actual_amount * train_amount / wanted_amount)
                test_amount = int(actual_amount * test_amount / wanted_amount)
            for file in os.listdir(tag):
                image = Image.open(tag + '/' + file)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image = image.resize((int(image.width * max_height / image.height), max_height))
                max_width = max(max_width, image.width)
            for file in os.listdir(tag):

                r = []
                g = []
                b = []
                image = Image.open(tag + '/' + file)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image = image.resize((int(image.width * max_height / image.height), max_height))
                if image.width > crop_width:
                    image = image.crop((0, 0, crop_width, image.height))
                old_r, old_g, old_b = image.split()
                old_r = np.array(old_r)
                for i in range(len(old_r)):
                    old_r[i] = old_r[i] / 255
                    print(f"{i} / {len(old_r)}")
                    r.append(np.concatenate((old_r[i], np.zeros(max_width - image.width))))
                r = np.array(r)
                old_g = np.array(old_g)
                for i in range(len(old_g)):
                    old_g[i] = old_g[i] / 255
                    g.append(np.concatenate((old_g[i], np.zeros(max_width - image.width))))
                g = np.array(g)
                old_b = np.array(old_b)
                for i in range(len(old_b)):
                    old_b[i] = old_b[i] / 255
                    b.append(np.concatenate((old_b[i], np.zeros(max_width - image.width))))
                b = np.array(b)
                if train_counter < train_amount:
                    train_data.append(np.array([r, g, b]))
                    train_tags.append(counter_tag)
                    train_counter += 1
                else:
                    test_data.append(np.array([r, g, b]))
                    test_tags.append(counter_tag)
                counter_tag += 1
        return np.array(train_data), np.array(train_tags), np.array(test_data), np.array(test_tags)


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
