import abc
from typing import List


class Plugin(abc.ABC):

    @abc.abstractmethod
    def info(self):
        pass

    @abc.abstractmethod
    def parse_requests(self, tags: List[str], amount: int = None) -> None:
        pass

    @abc.abstractmethod
    def parse_selenium(self, tags: List[str], amount: int = None) -> None:
        pass

    def parse(self, tags: List[str], amount=None) -> None:
        if amount is None:
            try:
                self.parse_requests(tags)
            except:
                self.parse_selenium(tags)
        else:
            try:
                self.parse_requests(tags, amount)
            except Exception as e:
                print(e)
                self.parse_selenium(tags, amount)
