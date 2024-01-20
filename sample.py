from image_parser import ImageParser

if __name__ == '__main__':
    data = {
        'cat': (1000, 200),  # (train, test
        'dog': (1000, 200),
    }
    parser = ImageParser(data)
    # parser.get_data()
    x_train, y_train, x_test, y_test = parser.load_data()
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)


