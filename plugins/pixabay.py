import time

import requests
import random
import string
import os
import urllib.request

from selenium.webdriver.common.by import By

import plugin
from bs4 import BeautifulSoup
import lxml
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager

class PixaBayPlugin(plugin.Plugin):

    def info(self):
        return '''Плагин для сбора данных с сервиса PixaBay. Делает запросы к сайту pixabay.com и парсит выдачу с помощью библиотеки BeautifulSoup.'''

    def parse(self, input_data: dict[str: int]) -> dict[str: int]:
        driver = uc.Chrome(executable_path="chromedriver.exe")
        images_per_page = 100
        url = "https://pixabay.com/images/search/{0}/?pagi={1}"
        result = {}
        counter = 0
        for tag in input_data:
            page = 1
            driver.get(url.format('cat', page))
            time.sleep(2) # ждем пока загрузится страница
            heading_text = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/section/p').text
            if heading_text == "Sorry, we couldn't find any matches":
                print(f"На сайте pixabay.com не нашлось картинок по тегу {tag}")
            else:
                pages = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[4]/div[3]/div')
                pages_num = int(pages.text.split()[-1])
                
            result[tag] = counter
        return result

PixaBayPlugin().parse({'cat': 10})