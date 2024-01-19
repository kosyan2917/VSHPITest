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
    parser.get_data()
    # print(parser.plugins)



