import plugin
import requests
import random
import urllib.request
import os


class PexelsPlugin(plugin.Plugin):
    PHOTOS_PER_PAGE = 80
    URL = "https://api.pexels.com/v1/search"

    def info(self):
        pass

    def parse_requests(self, tags: list, amount: int = 1500):
        print("ababa")
        api_key = "eRxahAyrePpfUuDuu9ejbK2nKmNMJzcBnBjbZoBnY1gakfmaGX0xbVDi"
        headers = {"Authorization": api_key}
        for query in tags:
            payload = {'query': query, 'per_page': self.PHOTOS_PER_PAGE, 'page': 1}
            page_num = amount // self.PHOTOS_PER_PAGE // len(tags)
            if not os.path.exists(query):
                os.mkdir(query)
            for page in range(1, page_num + 1):
                payload['page'] = page
                response = requests.get(self.URL, params=payload, headers=headers)
                print(response.json())
                photos = response.json()['photos']
                for photo in photos:
                    print(photo['src']['original'])
                    try:
                        opener = urllib.request.build_opener()
                        opener.addheaders = [
                            ('Authorization', 'eRxahAyrePpfUuDuu9ejbK2nKmNMJzcBnBjbZoBnY1gakfmaGX0xbVDi')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(photo['src']['original'], query + '/' + photo["alt"] + ".jpg")
                    except Exception as e:
                        print(e)
                        continue

    def parse_selenium(self, tags: list, amount: int = None):
        pass
