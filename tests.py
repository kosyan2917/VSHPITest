import urllib.request
url = "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg"

opener = urllib.request.build_opener()
opener.addheaders = [('Authorization', 'eRxahAyrePpfUuDuu9ejbK2nKmNMJzcBnBjbZoBnY1gakfmaGX0xbVDi')]
urllib.request.install_opener(opener)
urllib.request.urlretrieve(url, "local-filename.jpg")
