import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
# from time import sleep
import time
from tqdm import tqdm
# import better_exceptions

class Scraper(object):
    def __init__(self, url):
        self.url = url

    def make_request(self):
        response = requests.get(self.url, allow_redirects=True).content
        soup = BeautifulSoup(response, 'html.parser')
        return soup

    def get_images(self):
        raise NotImplementedError

    def album_name(self):
        raise NotImplementedError

    def download(self):
        # raise NotImplementedError

        images = self.get_images()
        # print(images)

        album = self.album_name()
        try:
            os.mkdir(album)
        except FileExistsError:
            pass
        # print('======', album, '======')
        # tqdm.write('======', album, '======')

        for index, image in enumerate(images):
            parsed = urlparse(image)
            filename = parsed.path.split('/')[-1]

            # r = requests.get(image, stream=True)

            if '.jpg' not in filename:
                filename = parsed.path.split('/')[-2] + '.jpg'

            full_path = album + '/' + filename


            def download_file(url, full_path, filename):
                """
                Helper method handling downloading large files from `url` to `filename`. Returns a pointer to `filename`.
                """
                chunkSize = 1024
                r = requests.get(url, stream=True)
                with open(full_path, 'wb') as f:
                    pbar = tqdm( unit="B", total=int( r.headers['Content-Length'] ), desc=album + ': ' + filename )
                    for chunk in r.iter_content(chunk_size=chunkSize):
                        if chunk: # filter out keep-alive new chunks
                            pbar.update (len(chunk))
                            f.write(chunk)


                time.sleep(1)

                # return filename


            download_file(image, full_path, filename)
        print('--------------')





            # break #test
        # pbar.write('-----------------------------------')
        # print('-----------------------------------')

        time.sleep(2)


class Fubiz(Scraper):
    def get_thumbnail(self):
        soup = self.make_request()
        for link in soup.find_all("a", class_="lightbox"):
            thumbnail = link.get('href') # return image wrapper url
            break

        try:
            # print(thumbnail)
            self.url = thumbnail
        except UnboundLocalError:
            for scrape in soup.find_all('div', class_='inner-post-content'):
                for link in scrape.find_all('a'):
                    continue
                thumbnail = link.get('href')
                redirect = requests.get(thumbnail)
                thumbnail = redirect.url
                # print(thumbnail)
                self.url = thumbnail

    def get_images(self):
        soup = self.make_request()
        images = [link.get('src') for link in soup.select('div > img')]
        return images

    def album_name(self):
        parsed = urlparse(self.url)
        album = parsed.path.split('/')[-3].replace('-', ' ').title()
        return album

class Kotaku(Scraper):
    def get_images(self):
        soup = self.make_request()
        images = []
        for image in soup.select('img[data-chomp-id]'):
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
        soup = self.make_request()
        images = []
        for link in soup.select('div > p > img'):
            src = link.get('src')
            images.append(src)

        if not images:
            for link in soup.select('div > p > span > img'):
                src = link.get('src')
                images.append(src)
        return images

    def album_name(self):
        parsed = urlparse(self.url)
        album = parsed.path.replace('-', ' ').title().replace('/', '')
        return album

class Popculturenexus(Scraper):
    def get_images(self):
        soup = self.make_request()
        images = []
        for link in soup.select('p > a > img'):
            try:
                image = link.get('data-orig-file').split('?')[0]
                images.append(image)
                # print(image)
            except AttributeError:
                pass

        return images

    def album_name(self):
        parsed = urlparse(self.url)
        album = parsed.path.split('/')[4].replace('-', ' ').title()
        return album

class Thedieline(Scraper):
    def get_images(self):
        if 'feed' in self.url:
            response = requests.get(self.url, allow_redirects=True)
            self.url = response.url.split('?')[0]
            # print(self.url)

        soup = self.make_request()
        images = []
        for scrape in soup.find_all(class_='sqs-layout sqs-grid-12 columns-12'):
            for link in scrape.find_all('img'):
                img = link.get('src')
                # print(img)
                images.append(img)

        images = [img for img in images if img]
        return images

    def album_name(self):
        parsed = urlparse(self.url)
        album = parsed.path.split('/')[-1].replace('-', ' ').title()
        return album

class HundredNudeShoots(Scraper):
    def get_images(self):
        soup = self.make_request()
        for scrape in soup.find_all('div', class_='entry-content'):
            images = scrape.find_all('img')
            images = [chunk.get('data-orig-file') for chunk in images]

        return images

    def album_name(self):
        parsed = urlparse(self.url)
        album = parsed.path.split('/')[-2].replace('-', ' ').title()
        return album

def main(filename):
    with open(filename, 'r') as f:
        sites = [line.strip() for line in f]

    for site in sites:
        if 'fubiz' in site:
            i = Fubiz(site)
            i.get_thumbnail()
            i.download()
        elif 'kotaku' in site:
            i = Kotaku(site)
            i.download()

        elif 'boredpanda' in site:
            i = Boredpanda(site)
            i.download()

        elif 'popculturenexus' in site:
            i = Popculturenexus(site)
            i.download()

        elif 'thedieline' in site:
            i = Thedieline(site)
            i.download()

        elif '100nudeshoots' in site:
            i = HundredNudeShoots(site)
            i.download()

main('urls.txt')

# """enum"""
# with open(album + '/' + str(index) + ' ' + filename, 'wb') as img_obj:



##########
            # total_size = int(r.headers.get('content-length', 0));
            # total_size = (int(r.headers.get('content-length', 0))/(32*1024))
            # with open(album + '/' + filename, 'wb') as f:
            #     for data in tqdm(r.iter_content(32*1024), total=total_size,
            #                      unit='B', unit_scale=True, desc=album + ': ' + filename):
            #         f.write(data)
#########




##################
            # chunkSize = 1024
            # with open(filename, 'wb') as f:
            #     pbar = tqdm( unit="B", total=int( r.headers['Content-Length'] ), unit_scale=True )
            #     pbar.set_description(album + ' ' + str(index))

            #     for chunk in r.iter_content(chunk_size=chunkSize):
            #         if chunk: # filter out keep-alive new chunks
            #             pbar.update (len(chunk))
            #             f.write(chunk)
#####################
            # total_size = int(r.headers["Content-Length"])
            # downloaded = 0  # keep track of size downloaded so far
            # chunkSize = 1024
            # bars = int(total_size / chunkSize)
            #
            # with open(album + '/' + filename, "wb") as f:
            #     pbar = tqdm(r.iter_content(chunk_size=chunkSize), total=bars, unit="KB",
            #                                   desc=filename, leave=True)
            #     for chunk in r.iter_content(chunk_size=chunkSize):
            #         f.write(chunk)
            #         downloaded += chunkSize  # increment the downloaded
            #         prog = ((downloaded * 100 / total_size))
            #         pbar.update(prog)  # *100 #Default max value of tkinter progress is 100


#######
            # total_size = int(r.headers["Content-Length"])
            # # downloaded = 0  # keep track of size downloaded so far
            # chunkSize = 1024
            # # bars = int(total_size / chunkSize)
            #
            # with open(album + '/' + filename, "wb") as f:
            #     pbar = tqdm(r.iter_content(chunk_size=chunkSize), total=total_size, unit="B",
            #                                   desc=filename, leave=True, unit_scale=True)
            #     for chunk in r.iter_content(chunk_size=chunkSize):
            #         f.write(chunk)
            #         pbar.update(len(chunk))  # *100 #Default max value of tkinter progress is 100
##################
