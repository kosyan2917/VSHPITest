import random
import urllib.request
from typing import List
import plugin
import requests
import os


class UnsplashPlugin(plugin.Plugin):

    URL = "https://api.unsplash.com/search/photos"
    PHOTOS_PER_PAGE = 30

    def info(self) -> str:
        return '''Плагин для сбора данных с сервиса Unsplash. Использует API сервиса Unsplash.
                На самом деле, используя его API, нельзя собирать данные для обучения нейронных сетей.'''

    def parse(self, input_data: dict[str: int]) -> dict[str: int]:
        result = {}
        unsplash_api_key = "lpfYpG8dpQRlB-b1SbvrTUC4OHIj5IJQzZ6C9Yd0nic"
        for tag in input_data:
            try:
                counter = 0
                amount = input_data[tag]
                payload = {'query': tag, 'client_id': unsplash_api_key, 'per_page': self.PHOTOS_PER_PAGE,
                           'order_by': 'popular', 'page': 1}
                page_num = amount // self.PHOTOS_PER_PAGE + 1
                if not os.path.exists(tag):
                    os.mkdir(tag)
                for page in range(1, page_num+1):
                    if counter == amount:
                        result[tag] = counter
                    payload['page'] = page
                    response = requests.get(self.URL, params=payload)
                    photos = response.json()['results']
                    for photo in photos:
                        print(photo['urls']['raw'])
                        urllib.request.urlretrieve(photo['urls']['raw'], tag + '/' + str(random.randint(1, 100000)) + ".jpg")
                        counter += 1
                        if counter == amount:
                            continue
                result[tag] = counter
            except Exception as e:
                print(f"Плагин Unsplash выдал ошибку {e} при скачивании картинок по тегу {tag}. Скачано картинок: {counter}")
                result[tag] = counter
        return result
