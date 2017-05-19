from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import os


def extract_image_urls(url):
    source_code = requests.get(url).content
    soup = BeautifulSoup(source_code, 'html.parser')

    images = []
    for image in soup.select('img[data-chomp-id]'):
        image_id = image.get('data-chomp-id')
        extension = image.get('data-format')
        images.append(image_id + '.' + extension)

    images = ['https://i.kinja-img.com/gawker-media/image/upload/' + image
              for image in images]

    return images

def create_dir(url):
    parsed = urlparse(url)
    album = ' '.join(parsed.path.split('-')[:-1]).title().replace('/', '')
    os.mkdir(album)
    print('====', album, 'created====')

    return album

def download(images, album):
    for image in images:
        parsed = urlparse(image)
        filename = parsed.path.split('/')[-1]

        image_b = requests.get(image)
        with open(album + '/' + filename, 'wb') as img_obj:
            img_obj.write(image_b.content)
        print(filename)

def main(url):
    images = extract_image_urls(url)
    print(images)

    album = create_dir(url)

    download(images, album)

    print('----------------')
