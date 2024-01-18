from ImageParser import ImageParser

if __name__ == '__main__':
    parser = ImageParser()
    # print(parser.plugins)
    parser.get_data({
        'cat': 50,
        'dog': 50,
    })
