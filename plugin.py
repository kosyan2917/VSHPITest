import abc
from typing import List


class Plugin(abc.ABC):

    @abc.abstractmethod
    def info(self):
        pass

    @abc.abstractmethod
    def parse(self, input_data: dict[str: int]) -> dict[str: int]:
        pass