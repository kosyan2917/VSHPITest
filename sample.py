from image_parser import ImageParser

if __name__ == '__main__':
    """
        Этот скрипт демонстрирует использование класса ImageParser для 
        скачивания картинок и их обработки для формирования наборов данных
        для машинного обучения.
    """

    data = {
        'cat': (1000, 200),  # (train, test
        'dog': (1000, 200),
    }
    try:
        parser = ImageParser(data)
        # parser.get_data()
        x_train, y_train, x_test, y_test = parser.load_data()
        print(x_train.shape)
        print(y_train.shape)
        print(x_test.shape)
        print(y_test.shape)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

