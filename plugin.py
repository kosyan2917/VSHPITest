import abc


class Plugin(abc.ABC):
    """Абстрактный класс для плагинов."""
    @abc.abstractmethod
    def info(self):
        """Получить информацию о плагине."""
        pass

    @abc.abstractmethod
    def parse(self, input_data: dict[str: int]) -> dict[str: int]:
        """
        Парсит изображения и возвращает количество скачанных изображений для каждого класса.

        Аргументы:
            input_data (dict[str: int]): Словарь, содержащий информацию о том, сколько картинок необходимо скачать
            для каждого класса.

        Возвращает:
            dict[str: int]: Словарь, содержащий информацию о том, сколько картинок было скачано.

        """
        pass