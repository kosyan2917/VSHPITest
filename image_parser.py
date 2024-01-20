import os.path
from typing import List, Type
from importlib import import_module
import numpy as np
import plugin
from PIL import Image, ImageFile


class ImageParser:

    def __init__(self, input_data: dict[str: tuple[int, int]]):
        self.input_data = input_data
        ImageFile.LOAD_TRUNCATED_IMAGES = True

    def get_info(self) -> None:
        plugins = self.load_plugins()
        for plug in plugins:
            print(plug.info())

    def get_data(self) -> dict[str: int]:
        plugins = self.load_plugins()
        plugins = plugins[:1]
        print(plugins)
        parse_data = {}
        for tag in self.input_data:
            parse_data[tag] = (self.input_data[tag][0] + self.input_data[tag][1]) // len(plugins)
        # plugins[1].parse(parse_data)
        for plug in plugins:
            print(plug.parse(parse_data))

    def load_data(self, height: int = 500, crop_width: int = None) -> (np.array, np.array, np.array, np.array):
        if crop_width is None:
            crop_width = height * 1.5
        train_data = []
        train_tags = []
        test_data = []
        test_tags = []
        print("Проверяю наличие картинок")
        for tag in self.input_data:
            counter_tag = 0
            train_counter = 0
            test_counter = 0
            if not os.path.exists(tag):
                raise FileNotFoundError(f"Папка с тегом {tag} не найдена. Возможно, вы не скачали картинки по тегу {tag}")
            wanted_amount = self.input_data[tag][0] + self.input_data[tag][1]
            actual_amount = len(os.listdir(tag))
            train_amount = self.input_data[tag][0]
            test_amount = self.input_data[tag][1]
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
                if image.width < image.height:
                    image = image.rotate(90, expand=1)
                image = image.resize((int(image.width * height / image.height), height))
                if image.width > crop_width:
                    image = image.crop((0, 0, crop_width, image.height))
                image_width = image.width
                # image.show()
                image = np.array(image, dtype=np.uint8)
                new_r, new_g, new_b = [], [], []
                for i in range(height):
                    new_r.append(np.concatenate((image[i][:, 0], np.zeros(int(crop_width - image_width), dtype=np.uint8))))
                    new_g.append(np.concatenate((image[i][:, 1], np.zeros(int(crop_width - image_width), dtype=np.uint8))))
                    new_b.append(np.concatenate((image[i][:, 2], np.zeros(int(crop_width - image_width), dtype=np.uint8))))
                new_r = np.array(new_r)
                new_g = np.array(new_g)
                new_b = np.array(new_b)
                new_image = np.array([new_r, new_g, new_b], dtype=np.uint8)
                new_image = np.transpose(new_image, (1, 2, 0))
                new_image = Image.fromarray(new_image.astype('uint8'))
                # new_image.show()
                if train_counter < train_amount:
                    train_data.append(new_image)
                    train_tags.append(counter_tag)
                    train_counter += 1
                else:
                    test_data.append(new_image)
                    test_tags.append(counter_tag)
                    test_counter += 1
                    if test_counter == test_amount:
                        break
                counter_tag += 1
                print(f"Обработано {counter_tag} картинок из {wanted_amount} по тегу {tag}")
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
