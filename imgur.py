import requests
from bs4 import BeautifulSoup, NavigableString
import re


def parse_album(album_id):
    addr = 'http://imgur.com/a/' + album_id
    # print(addr)
    r = requests.get(addr)
    soup = BeautifulSoup(r.text, "html.parser")
    href = soup.find('div', {"class": "post-image"}).a['href']
    return 'http://' + href


def image(content, cat='main'):
    if cat == 'thumb':
        tag = "<div class='row'><div class='thumbnail col-xs-6 col-xs-offset-1'>"
        endtag = "</div></div>"
    else:
        tag = ''
        endtag = ''
    m = re.search('http.*://.*imgur.com/(\w+)(\.jpg)*(.*)', content)
    if m:  # image link
        if m.group(1) == 'a':
            href = parse_album(m.group(3)[1:6])
        else:
            href = 'http://i.imgur.com/' + m.group(1) + '.jpg'
        html = tag
        html += "<a href= '" + href + "'>" + content
        html += "<img src='" + href + "' title='" + href + "' class='img-rounded img-responsive'>"
        html += endtag + "</a>"

        return html
    else:  # hyperlink
        m = re.search('(.*)(http.*://.*)( *.*)', content)
        if m:
            html = m.group(1)
            html += "<a href= '" + m.group(2) + "'>" + m.group(2) + "</a>"
            html += m.group(3)
            content = html

        return content
