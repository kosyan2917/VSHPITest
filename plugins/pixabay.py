import time

import requests
import random
import string
import os
import urllib.request
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import plugin
from bs4 import BeautifulSoup
import lxml
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager


class PixaBayPlugin(plugin.Plugin):

    def info(self):
        return '''Плагин для сбора данных с сервиса PixaBay. 
        Парсинг проводится с помощью Selenium, во время работы открывает браузер.'''

    def parse(self, input_data: dict[str: int]) -> dict[str: int]:
        driver = uc.Chrome()
        images_per_page = 100
        url = "https://pixabay.com/images/search/{0}/?pagi={1}"
        result = {}
        for tag in input_data:
            try:
                if not os.path.exists(tag):
                    os.mkdir(tag)
                counter = 0
                amount = input_data[tag]
                page = 1
                flag = True
                while flag:
                    time.sleep(2)
                    driver.get(url.format(tag, page))
                    driver_cookies = driver.get_cookies()
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', driver.execute_script("return navigator.userAgent"))]
                    urllib.request.install_opener(opener)
                    # Ждем пока загрузится страница
                    while True:
                        try:
                            heading_text = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/section/p').text
                            break
                        except Exception as e:
                            time.sleep(2)
                    time.sleep(3) # Ждем пока загрузятся все картинки
                    if heading_text == "Sorry, we couldn't find any matches":
                        print(f"На сайте pixabay.com не нашлось картинок по тегу {tag}")
                    else:
                        pages = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[4]/div[3]/div')
                        pages_num = int(pages.text.split()[-1])
                        found_amount = pages_num * images_per_page
                        if amount > found_amount:
                            print(f"На сайте pixabay.com не нашлось {amount} картинок по тегу {tag}. Нашлось {found_amount}")
                            amount = found_amount
                        for cur_pos in range(0, 10000, 500):
                            driver.execute_script("window.scrollTo(0, {});".format(cur_pos))
                            time.sleep(0.1)
                        photos = driver.find_elements(By.XPATH, ".//a[@class='link--WHWzm']/img")
                        for photo in photos:
                            photo_src = photo.get_attribute('src')
                            if photo_src.startswith('https'):
                                urllib.request.urlretrieve(photo_src, tag + '/' + "pixabay-" + str(random.randint(1, 100000)) + ".jpg")
                                counter += 1
                                if counter == amount:
                                    flag = False
                                    result[tag] = counter
                                    break
                                print(f"Плагин pixabay скачал {counter} картинок из {amount} по тегу {tag}")
                        page += 1
                    result[tag] = counter
            except Exception as e:
                print(f"Плагин pixabay выдал ошибку {e} при скачивании картинок по тегу {tag}. Скачано {counter} картинок")
                result[tag] = counter
        return result

