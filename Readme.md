# Что это

Это скрипт, который парсит открытые источники картинок, прописанные в плагинах, по заданным тэгам.

## Как пользоваться

Помотреть пример использования можно в файле sample.py
1. Установите зависимости из requirements.txt
2. Импортируйте класс ImageParser из файла image_parser.py
3. Создайте экземпляр класса ImageParser, передав в него словарь тэгов, по которым будет производиться поиск.

    Данные нужно подавать в виде:
    ```
    {
        "tag1": {
            "train": amount,
            "test": amount
        },
        "tag2": {
            "train": amount,
            "test": amount
        },
    }
    ```
4. Вызовите метод get_data(), чтобы скачать картинки по заданным тэгам
5. Вызовите метод load_data(), чтобы загрузить картинки из диска в память

Метод get_data() словарь, где ключом является метка класса, а значением - количество скачанных картинок

## Как добавить свой плагин

1. Создайте отдельный .py файл для вашего плагина 
2. Создайте класс, наследованный от класса Plugin, расположенного в корне проекта, реализуйте необходимые методы
3. Добавьте свой файл с плагином в папку plugins. 

## Текущие необходимые улучшения:

- Создать больше плагинов
- Запускать плагины асинхронно
- Добавить проверки на количество найденного фото
