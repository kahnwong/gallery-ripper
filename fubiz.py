import urllib.request
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import os

def fubiz_dl(url):
    
    #~ """Extract images off the page (if exist)"""
    #~ source_code = requests.get(url, allow_redirects=True)
    #~ plain_text = source_code.text.encode('ascii', 'replace')
    #~ soup = BeautifulSoup(plain_text,'html.parser')
    #~ imgs_off_frontpage = []
    
    #~ for link in soup.select('p > img'):
        #~ data_original = link.get('data-original')
        #~ imgs_off_frontpage.append(data_original)
    

    """Extract gallery url"""
    source_code = requests.get(url, allow_redirects=True)
    plain_text = source_code.text.encode('ascii', 'replace')
    soup = BeautifulSoup(plain_text,'html.parser')
    thumbnail = ''  # if the first soup doesnt work the second one has 
                    # something to compare to
    
    for link in soup.find_all("a", class_="lightbox"):
        href = link.get('href')
        thumbnail = href
        break
    
    if not thumbnail:
        thumbnails = []
        for link in soup.select('p > a'):
            href = link.get('href')
            thumbnails.append(href)
        thumbnail = thumbnails[3]
        
    print(thumbnail)
    
    """Create dir"""
    parsed = urlparse(thumbnail)
    album = parsed.path.split('/')[-3].replace('-', ' ').title()
    os.mkdir(album)
    
    """Extract image urls"""
    source_code = requests.get(thumbnail, allow_redirects=True)
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
