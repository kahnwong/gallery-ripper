import urllib.request
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import os

def kotaku_artwork_dl(url):

    """Create dir"""
    parsed = urlparse(url)
    album = ' '.join(parsed.path.split('-')[:-1]).title().replace('/', '')
    os.mkdir(album)

    """Extract image urls"""
    source_code = requests.get(url, allow_redirects=True)
    plain_text = source_code.text.encode('ascii', 'replace')
    soup = BeautifulSoup(plain_text,'html.parser')
    images = []
    
    #~ for image in soup.find_all("p", class_="ls-lazy-image-tag cursor-pointer lazyautosizes lazyloaded"):
    for image in soup.select('img[data-chomp-id]'):
        image_id = image.get('data-chomp-id')
        extension = image.get('data-format')
        images.append(image_id + '.' + extension)
    print(images)
    
    """Download images"""
    for image in images:
        image_url = 'https://i.kinja-img.com/gawker-media/image/upload/' + image
        parsed = urlparse(image_url)
        filename = parsed.path.split('/')[-1]
        urllib.request.urlretrieve(image_url, album + '/' + filename)
        print('Download', filename, 'completed')

    print("------Download", album, "completed!------")
