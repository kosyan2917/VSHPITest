import random
import urllib.request
from typing import List
import plugin
import requests
import os


class UnsplashPlugin(plugin.Plugin):

    URL = "https://api.unsplash.com/search/photos"
    PHOTOS_PER_PAGE = 5

    def info(self):
        pass

    def parse_requests(self, tags: List[str], amount: int = 1500):
        """Парсинг выдачи сервиса Unsplash. На самом деле, используя его API, нельзя собирать
                данные для обучения"""
        unsplash_api_key = "lpfYpG8dpQRlB-b1SbvrTUC4OHIj5IJQzZ6C9Yd0nic"
        for query in tags:

            payload = {'query': query, 'client_id': unsplash_api_key, 'per_page': self.PHOTOS_PER_PAGE,
                       'order_by': 'popular', 'page': 1}
            page_num = amount // self.PHOTOS_PER_PAGE // len(tags)
            if not os.path.exists(query):
                os.mkdir(query)
            for page in range(1, page_num+1):
                payload['page'] = page
                response = requests.get(self.URL, params=payload)
                photos = response.json()['results']
                for photo in photos:
                    print(photo['urls']['raw'])
                    urllib.request.urlretrieve(photo['urls']['raw'], query + '/' + str(random.randint(1, 100000)) + ".jpg")

    def parse_selenium(self, tags: List[str], amount: int = None):
        raise NotImplementedError("Данный плагин не поддерживает Selenium")