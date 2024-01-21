import plugin
import requests
import random
import urllib.request
import os


class PexelsPlugin(plugin.Plugin):
    PHOTOS_PER_PAGE = 80
    URL = "https://api.pexels.com/v1/search"

    def info(self) -> str:
        return '''Плагин для сбора данных с сервиса Pexels. Использует API сервиса Pexels.'''

    def parse(self, input_data: dict[str: int]) -> dict[str: int]:
        api_key = "eRxahAyrePpfUuDuu9ejbK2nKmNMJzcBnBjbZoBnY1gakfmaGX0xbVDi"
        headers = {"Authorization": api_key}
        result = {}
        for tag in input_data:
            try:
                counter = 0
                amount = input_data[tag]
                payload = {'query': tag, 'per_page': self.PHOTOS_PER_PAGE, 'page': 1}
                page_num = amount // self.PHOTOS_PER_PAGE + 1
                if not os.path.exists(tag):
                    os.mkdir(tag)
                for page in range(1, page_num + 1):
                    if counter == amount:
                        result[tag] = counter
                        break
                    payload['page'] = page
                    response = requests.get(self.URL, params=payload, headers=headers)
                    if response.json()['total_results'] < amount:
                        amount = response.json()['total_results']
                    photos = response.json()['photos']
                    for photo in photos:
                        opener = urllib.request.build_opener()
                        opener.addheaders = [
                            ('Authorization', api_key)]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(photo['src']['original'], tag + '/' + photo["alt"] + ".jpg")
                        counter += 1
                        if counter == amount:
                            break
                        print(f"Плагином pexels скачано {counter} картинок из {amount} по тегу {tag} ")
                result[tag] = counter
            except Exception as e:
                print(
                    f"Плагин Pexels выдал ошибку {e} при скачивании картинок по тегу {tag}. Скачано картинок: {counter}")
                result[tag] = counter
        return result
