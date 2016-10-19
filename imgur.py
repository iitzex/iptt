import requests
from bs4 import BeautifulSoup, NavigableString


def parse_album(album_id):
    addr = 'http://imgur.com/a/' + album_id
    # print(addr)
    r = requests.get(addr)
    soup = BeautifulSoup(r.text, "html.parser")
    href = soup.find('div', {"class": "post-image"}).a['href']
    return 'http://' + href

