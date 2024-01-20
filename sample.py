from image_parser import ImageParser

if __name__ == '__main__':
    data = {
        'cat': {
            'train': 100,
            'test': 20
        },
        'dog': {
            'train': 100,
            'test': 20
        },
    }
    parser = ImageParser(data)
    # parser.get_data()
    x_train, y_train, x_test, y_test = parser.load_data()
    print(x_train.shape)
    print(x_test.shape)
    # print(parser.plugins)



