import os
import random
import urllib.request
import plugin
import requests
from bs4 import BeautifulSoup
import lxml


class FreeImagesPlugin(plugin.Plugin):

    URL = "https://www.freeimages.com/search/{0}/{1}"

    def info(self) -> str:
        return '''Плагин для сбора данных с сервиса freeimages. Делает запросы к сайту freeimages.com и парсит 
        выдачу с помощью библиотеки BeautifulSoup.'''

    def parse(self, input_data: dict[str: int]) -> dict[str: int]:
        result = {}
        for tag in input_data:
            try:
                amount = input_data[tag]
                if not os.path.exists(tag):
                    os.mkdir(tag)
                page = 1
                counter = 0
                flag = True
                while flag:
                    response = requests.get(self.URL.format(tag, page))
                    html_page = BeautifulSoup(response.text, 'lxml')
                    no_contents = html_page.find('p', class_='text-3xl')
                    if no_contents is not None:
                        print(html_page.find('p', class_='text-3xl').text)
                        print(f"Кончились картинки для {tag}")
                        break
                    try:
                        h1 = html_page.find('h1', class_='text-gray-font text-3xl').text
                        found_amount = int(h1.split()[0])
                    except Exception as e:
                        print(e)
                        print(f"Вероятно на сайте freeimage не нашлось картинок по тегу {tag}")
                        flag = False
                        continue
                    grid_container = html_page.find('div', class_='grid-container')
                    photos = grid_container.find_all('div', class_='grid-item')
                    for photo in photos:
                        image_url = photo.find('img')['src']
                        if image_url.startswith('https'):
                            urllib.request.urlretrieve(image_url, tag + '/' + str(random.randint(1, 100000)) + ".jpg")
                            counter += 1
                            if counter == amount:
                                flag = False
                                result[tag] = counter
                                break
                            print(f"Плагин freeimages скачал {counter} картинок из {amount} по тегу {tag}")
                    page += 1
                result[tag] = counter
            except Exception as e:
                print(f"Плагин freeimages выдал ошибку {e} при скачивании картинок по тегу {tag}. Скачано {counter} картинок")
                result[tag] = counter
        return result
