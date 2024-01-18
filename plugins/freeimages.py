import plugin
import requests


class FreeImagesPlugin(plugin.Plugin):

    URL = "https://www.freeimages.com/search/{0}/{1}"

    def info(self):
        pass

    def parse_requests(self, tags: list, amount: int = None):
        for tag in tags:
            page = 1
            response = requests.get(self.URL.format(tag, page))
            print(response.text)

    def parse_selenium(self, tags: list, amount: int = None):
        pass