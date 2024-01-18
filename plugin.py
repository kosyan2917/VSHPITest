import abc
from typing import List


class Plugin(abc.ABC):

    @abc.abstractmethod
    def info(self):
        pass

    @abc.abstractmethod
    def parse_requests(self, input_data: dict[str: int]) -> None:
        pass

    @abc.abstractmethod
    def parse_selenium(self, input_data: dict[str: int]) -> None:
        pass

    def parse(self, input_data: dict[str: int]) -> None:
        try:
            self.parse_requests(input_data)
        except Exception as e:
            print(e)
            self.parse_selenium(input_data)
