import urllib.request
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import os

def fubiz_dl(url):

    """Extract gallery url"""
    source_code = requests.get(url, allow_redirects=True)
    plain_text = source_code.text.encode('ascii', 'replace')
    soup = BeautifulSoup(plain_text,'html.parser')
    thumbnails = []
    
    for link in soup.find_all("a", class_="lightbox"):
        href = link.get('href')
        thumbnails.append(href)
    
    """Create dir"""
    parsed = urlparse(thumbnails[0])
    album = parsed.path.split('/')[-3].replace('-', ' ').title()
    os.mkdir(album)
    
    """Extract image urls"""
    source_code = requests.get(thumbnails[0], allow_redirects=True)
    plain_text = source_code.text.encode('ascii', 'replace')
    soup = BeautifulSoup(plain_text,'html.parser')
    urls = []
    
    for link in soup.select('div > img'):
        src = link.get('src')
        urls.append(src)

    """Download images"""
    for url in urls:
        parsed = urlparse(url)
        filename = parsed.path.split('/')[-1]
        urllib.request.urlretrieve(url, album + '/' + filename)
        print('Download', filename, 'completed!')

    print("----Download", album, "completed!----")
