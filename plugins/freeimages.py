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
            page = 1

            response = requests.get(self.URL.format(tag, page))
            html_page = BeautifulSoup(response.text, 'lxml')
            h1 = html_page.find('h1', class_='text-gray-font text-3xl').text
            found_amount = int(h1.split()[0])
            print(found_amount)
            return
            grid_container = html_page.find('div', class_='grid-container')
            print(grid_container)
            photos = grid_container.find_all('div', class_='grid-item')
            print(len(photos))
            for photo in photos:
                image_url = photo.find('img')['src']
                print(photo.find('img')['src'])
                if image_url.startswith('https'):
                    urllib.request.urlretrieve(image_url, tag + '/' + str(random.randint(1, 100000)) + ".jpg")



    def parse_selenium(self, tags: list, amount: int = None):
        pass