import unittest
from unittest.mock import patch
from image_parser import ImageParser
import numpy as np


class TestImageParser(unittest.TestCase):

    def setUp(self):
        self.input_data = {
            'tag1': (10, 5),
            'tag2': (8, 4),
        }
        self.parser = ImageParser(self.input_data)

    def test_init_with_empty_input_data(self):
        with self.assertRaises(ValueError):
            ImageParser({})

    def test_init_with_empty_tag(self):
        with self.assertRaises(ValueError):
            ImageParser({'': (10, 5)})

    def test_init_with_negative_values(self):
        with self.assertRaises(ValueError):
            ImageParser({'tag1': (-10, 5)})

    def test_load_data_with_missing_folder(self):
        height = 500
        crop_width = None
        self.input_data['InvalidTag'] = (10, 5)
        with self.assertRaises(FileNotFoundError):
            self.parser.load_data(height, crop_width)

    def test_load_plugins(self):
        plugins = self.parser.load_plugins()
        self.assertIsInstance(plugins, list)
        self.assertGreater(len(plugins), 0)
        for plugin in plugins:
            self.assertTrue(hasattr(plugin, 'info'))
            self.assertTrue(hasattr(plugin, 'parse'))

    def test_load_data_with_plugins_input(self):
        with self.assertRaises(ModuleNotFoundError):
            ImageParser(self.input_data, plugins=['InvalidPlugin'])


if __name__ == '__main__':
    unittest.main()
