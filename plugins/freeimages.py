import os
import random
import urllib.request
import plugin
import requests
from bs4 import BeautifulSoup
import lxml


class FreeImagesPlugin(plugin.Plugin):

    URL = "https://www.freeimages.com/search/{0}/{1}"

    def info(self):
        pass

    def parse_requests(self, tags: list, amount: int = None):
        for tag in tags:
            if not os.path.exists(tag):
                os.mkdir(tag)
            page = 71
            count = 0
            while True:
                if count == amount:
                    break
                response = requests.get(self.URL.format(tag, page))
                html_page = BeautifulSoup(response.text, 'lxml')
                no_contents = html_page.find('p', class_='text-3xl')
                print(no_contents)
                if no_contents is not None:
                    print(html_page.find('p', class_='text-3xl').text)
                    print(f"Кончились картинки для {tag}")
                    break
                try:
                    h1 = html_page.find('h1', class_='text-gray-font text-3xl').text
                    found_amount = int(h1.split()[0])
                except:
                    print(f"Вероятно на сайте freeimage не нашлось картинок по тегу {tag}")
                    continue
                print(found_amount)
                grid_container = html_page.find('div', class_='grid-container')
                print(grid_container)
                photos = grid_container.find_all('div', class_='grid-item')
                print(len(photos))
                for photo in photos:
                    image_url = photo.find('img')['src']
                    print(photo.find('img')['src'])
                    if image_url.startswith('https'):
                        urllib.request.urlretrieve(image_url, tag + '/' + str(random.randint(1, 100000)) + ".jpg")
                        count += 1


    def parse_selenium(self, tags: list, amount: int = None):
        pass