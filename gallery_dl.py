import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
# import better_exceptions

class Scraper(object):
    def __init__(self, url):
        self.url = url

    def make_request(self):
        self.response = requests.get(self.url, allow_redirects=True).content
        self.soup = BeautifulSoup(self.response, 'html.parser')
        return self.soup

    def get_images(self):
        raise NotImplementedError

    def album_name(self):
        raise NotImplementedError

    def download(self):
        # raise NotImplementedError

        album = self.album_name()
        os.mkdir(album)
        print('======', album, '======')
        images = self.get_images()
        print(images)

        for image in images:
            parsed = urlparse(image)
            filename = parsed.path.split('/')[-1]

            image_b = requests.get(image)
            with open(album + '/' + filename, 'wb') as img_obj:
                img_obj.write(image_b.content)
            print(filename)
            # break #test
        print('-----------------------------------')


class Fubiz(Scraper):
    def get_thumbnail(self):
        for link in self.soup.find_all("a", class_="lightbox"):
            thumbnail = link.get('href') # return image wrapper url
            break

        try:
            print(thumbnail)
            self.url = thumbnail
        except UnboundLocalError:
            for scrape in self.soup.find_all('div', class_='inner-post-content'):
                for link in scrape.find_all('a'):
                    continue
                thumbnail = link.get('href')
                redirect = requests.get(thumbnail)
                thumbnail = redirect.url
                print(thumbnail)
                self.url = thumbnail


    def get_images(self):
        soup = super().make_request()
        images = [link.get('src') for link in soup.select('div > img')]
        return images

    def album_name(self):
        parsed = urlparse(self.url)
        album = parsed.path.split('/')[-3].replace('-', ' ').title()
        return album

class Kotaku(Scraper):
    def get_images(self):
        images = []
        for image in self.soup.select('img[data-chomp-id]'):
            image_id = image.get('data-chomp-id')
            extension = image.get('data-format')
            images.append(image_id + '.' + extension)

        images = ['https://i.kinja-img.com/gawker-media/image/upload/' + image for image in images]
        return images

    def album_name(self):
        parsed = urlparse(self.url)
        album = ' '.join(parsed.path.split('-')[:-1]).title().replace('/', '')
        return album

class Boredpanda(Scraper):
    def get_images(self):
        images = []
        for link in self.soup.select('div > p > img'):
            src = link.get('src')
            images.append(src)

        # if len(images) == 0:
        if not images:
            for link in self.soup.select('div > p > span > img'):
                src = link.get('src')
                images.append(src)
        return images

    def album_name(self):
        parsed = urlparse(self.url)
        album = parsed.path.replace('-', ' ').title().replace('/', '')
        return album



def main(filename):
    with open(filename, 'r') as f:
        sites = [line.strip() for line in f]
    # print(sites)

    for site in sites:
        if 'fubiz' in site:
            i = Fubiz(site)
            i.make_request()
            i.get_thumbnail()
            i.download()
        elif 'kotaku' in site:
            i = Kotaku(site)
            i.make_request()
            i.download()

        elif 'boredpanda' in site:
            i = Boredpanda(site)
            i.make_request()
            i.download()

main('urls.txt')
