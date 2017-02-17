from urllib.parse import urlparse
import boredpanda
import fubiz
import kotaku

def main(urls):

    """Load urls"""

    with open (urls, 'r') as f:
        album_urls = [line.strip() for line in f]

    """Check website"""

    for album_url in album_urls:
        parsed = urlparse(album_url)
        site = parsed.netloc

        if 'boredpanda' in site:
            boredpanda.boredpanda_dl(album_url)
        if 'fubiz' in site:
            fubiz.fubiz_dl(album_url)
        if 'kotaku' in site:
            kotaku.kotaku_artwork_dl(album_url)

main('urls.txt')
