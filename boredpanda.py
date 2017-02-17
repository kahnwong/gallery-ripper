import urllib.request
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import os

def boredpanda_dl(url):

    """Create dir"""
    parsed = urlparse(url)
    album = parsed.path.replace('-', ' ').title().replace('/', '')
    os.mkdir(album)

    """Extract image urls"""
    source_code = requests.get(url, allow_redirects=True)
    plain_text = source_code.text.encode('ascii', 'replace')
    soup = BeautifulSoup(plain_text,'html.parser')
    urls = []
    for link in soup.select('div > p > img'):
        src = link.get('src')
        urls.append(src)
        
    if len(urls) == 0:
        for link in soup.select('div > p > span > img'):
            src = link.get('src')
            urls.append(src)

    """Download images"""
    for url in urls:
        parsed = urlparse(url)
        filename = parsed.path.split('/')[-1]
        urllib.request.urlretrieve(url, album + '/' + filename)
        print('Download', filename, 'completed!')

    print("----Download", album, "completed!----")
