import boredpanda
import fubiz
import kotaku
import popculturenexus

def main(urls):

    """Load urls"""

    with open (urls, 'r') as f:
        sites = [line.strip() for line in f]

    """Check website"""

    for album_url in sites:
        if 'boredpanda' in album_url:
            boredpanda.boredpanda_dl(album_url)
        if 'fubiz' in album_url:
            #~ fubiz_ptoimg.fubiz_dl(album_url)
            fubiz.main(album_url)
            # break
        if 'kotaku' in album_url:
            kotaku.main(album_url)
            break

        if 'popculturenexus' in album_url:
            popculturenexus.popculturenexus_dl(album_url)


main('urls.txt')
# main('kotaku.txt')
