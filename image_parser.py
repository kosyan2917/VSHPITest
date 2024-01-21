import os.path
from typing import List, Type
from importlib import import_module
import numpy as np
import plugin
from PIL import Image, ImageFile


class ImageParser:
    """
        Класс для парсинга изображений из открытых источников на основе входных данных.

        Атрибуты:
            input_data (dict[str: tuple[int, int]]): Словарь, содержащий информацию о том, какие картинки и
            какое количество необходимо искать.
        Методы:
            __init__(self, input_data: dict[str: tuple[int, int]]): Конструктор класса ImageParser.

            get_info(self) -> None: Печатает информацию о плагине в консоль.

            get_data(self) -> dict[str: int]: Парсит изображения и возвращает количетсво скачанных изображений
            для каждого класса.

            load_data(self, height: int = 500, crop_width: int = None) -> (np.array, np.array, np.array, np.array):
                Загружает данные в пямять в виде массивов numpy.

            load_plugins() -> List[plugin.Plugin]: Загружает плагины из папки plugins.
        """

    def __init__(self, input_data: dict[str: tuple[int, int]]):
        self.input_data = input_data
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        if not input_data:
            raise ValueError("Словарь с данными не может быть пустым")
        for tag in input_data:
            if not tag:
                raise ValueError("Тег не может быть пустым")
            if len(input_data[tag]) != 2:
                raise ValueError("Каждому тегу должно соответствовать два числа: "
                                 "число картинок для обучения и число картинок для тестирования")
            if input_data[tag][0] < 1 or input_data[tag][1] < 1:
                raise ValueError("Число картинок не может быть меньше 1")

    def get_info(self) -> None:
        """Печатает информацию о плагине в консоль."""
        plugins = self.load_plugins()
        for plug in plugins:
            print(plug.info())

    def get_data(self) -> dict[str: int]:
        """
            Парсит изображения и возвращает количетсво скачанных изображений
            для каждого класса.

            Возвращает:
                dict[str: int]: Словарь, содержащий информацию о том, сколько изображений было скачано для каждого класса.
        """
        plugins = self.load_plugins()
        plugins = plugins[:1]
        result = {}
        print(plugins)
        parse_data = {}
        for tag in self.input_data:
            parse_data[tag] = (self.input_data[tag][0] + self.input_data[tag][1]) // len(plugins)
        # plugins[1].parse(parse_data)
        for plug in plugins:
            parsed = plug.parse(parse_data)
            for tag in parsed:
                if tag not in result:
                    result[tag] = 0
                result[tag] += parsed[tag]
        return result

    def load_data(self, height: int = 500, crop_width: int = None) -> (np.array, np.array, np.array, np.array):
        """
            Загружает данные в пямять в виде массивов numpy.

            Аргументы:
                height (int): Высота выходного изображения. По умолчанию 500.

                crop_width (int): Ширина выходного изображения. По умолчанию 1.5 * height.

            Возвращает:
                (np.array, np.array, np.array, np.array): Кортеж из четырех массивов numpy:
                train_data, train_tags, test_data, test_tags. Первые два массива содержат данные для обучения,
                вторые два - для тестирования.
        """
        if crop_width is None:
            crop_width = height * 1.5
        train_data = []
        train_tags = []
        test_data = []
        test_tags = []
        print("Проверяю наличие картинок")
        for tag in self.input_data:
            # Заводим переменные для подсчета количества картинок
            counter_tag = 0
            train_counter = 0
            test_counter = 0
            # Проверяем наличие папки с тегом
            if not os.path.exists(tag):
                raise FileNotFoundError(f"Папка с тегом {tag} не найдена. Возможно, вы не скачали картинки по тегу {tag}")
            # Проверяем, что в папке с тегом хватит картинок, и если нет, то собираем данные пропорционально
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
            # Перебираем все картинки в папке с тегом
            for file in os.listdir(tag):
                image = Image.open(tag + '/' + file)
                # Проверяем, что картинка в формате RGB, иначе преобразуем в RGB
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                # Если картинка в портретной ориентации, то поворачиваем ее
                if image.width < image.height:
                    image = image.rotate(90, expand=1)
                # Изменяем высоту картинки до заданной, ширину - пропорционально
                image = image.resize((int(image.width * height / image.height), height))
                # Обрезаем картинку до заданной ширины, если она больше
                if image.width > crop_width:
                    image = image.crop((0, 0, crop_width, image.height))
                image_width = image.width
                image = np.array(image, dtype=np.uint8)
                new_r, new_g, new_b = [], [], []
                # Разделяем картинку на три канала и добавляем в каждую строку картинки нули до заданной ширины
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
        """
            Загружает плагины из папки plugins

            Возвращает:
                List[plugin.Plugin]: Список загруженных плагинов
        """
        loaded_plugins = []
        plugs = os.listdir('plugins')
        for plug in plugs:
            if plug.endswith('.py'):
                import_module('plugins.' + plug[:-3])
        for plug in plugin.Plugin.__subclasses__():
            loaded_plugins.append(plug())
        return loaded_plugins
