import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def s(i):
    source_code = requests.get(i, allow_redirects=True).content
    soup = BeautifulSoup(source_code, 'html.parser')
    return soup

def get_thumbnail_url(url):
    soup = s(url)
    for link in soup.find_all("a", class_="lightbox"):
        thumbnail = link.get('href') # return all images wrapper url
        break

    try:
        print(thumbnail)
        return thumbnail
    except UnboundLocalError:
        for scrape in soup.find_all('div', class_='inner-post-content'):
            for link in scrape.find_all('a'):
                continue
            thumbnail = link.get('href')
            redirect = requests.get(thumbnail)
            thumbnail = redirect.url
            print(thumbnail)
            return thumbnail

def create_dir(thumbnail):
    parsed = urlparse(thumbnail)
    album = parsed.path.split('/')[-3].replace('-', ' ').title()
    os.mkdir(album)

    print('====', album, 'created====')
    return album

def extract_image_urls(thumbnail):
    soup = s(thumbnail)
    images = [link.get('src') for link in soup.select('div > img')]
    print(images)
    return images

def download(images, album):
    for image in images:
        parsed = urlparse(image)
        filename = parsed.path.split('/')[-1]

        image_b = requests.get(image)
        with open(album + '/' + filename, 'wb') as img_obj:
            img_obj.write(image_b.content)
        print(filename)
        # break #test

def main(url):
    thumbnail = get_thumbnail_url(url)
    images = extract_image_urls(thumbnail)
    album = create_dir(thumbnail)
    download(images, album)

    print('----------------')
