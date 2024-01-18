import plugin
import requests
import random
import urllib.request
import os


class PexelsPlugin(plugin.Plugin):
    PHOTOS_PER_PAGE = 80
    URL = "https://api.pexels.com/v1/search"

    def info(self):
        return '''Плагин для сбора данных с сервиса Pexels. Использует API сервиса Pexels.'''

    def parse_requests(self, input_data: dict[str: int]) -> None:
        print("ababa")
        api_key = "eRxahAyrePpfUuDuu9ejbK2nKmNMJzcBnBjbZoBnY1gakfmaGX0xbVDi"
        headers = {"Authorization": api_key}
        for tag in input_data:
            counter = 0
            print('aaa')
            amount = input_data[tag]
            payload = {'query': tag, 'per_page': self.PHOTOS_PER_PAGE, 'page': 1}
            page_num = amount // self.PHOTOS_PER_PAGE + 1
            if not os.path.exists(tag):
                os.mkdir(tag)
            for page in range(1, page_num + 1):
                if counter == amount:
                    break
                payload['page'] = page
                response = requests.get(self.URL, params=payload, headers=headers)
                if response.json()['total_results'] < amount:
                    amount = response.json()['total_results']
                print(response.json())
                photos = response.json()['photos']
                for photo in photos:
                    print(photo['src']['original'])
                    opener = urllib.request.build_opener()
                    opener.addheaders = [
                        ('Authorization', api_key)]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(photo['src']['original'], tag + '/' + photo["alt"] + ".jpg")
                    counter += 1
                    if counter == amount:
                        continue

    def parse_selenium(self, tags: list, amount: int = None):
        pass
