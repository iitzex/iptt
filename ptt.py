import requests
from collections import OrderedDict
from bs4 import BeautifulSoup, NavigableString
import re
DEBUG = True


def pprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def parse_post(board, post):
    addr = 'https://www.ptt.cc/bbs/' + board + '/' + post
    r = requests.get(addr)
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find('div', id="main-content")

    post = OrderedDict()
    text = []
    # print(addr)

    for item in div.contents:
        if isinstance(item, NavigableString):
            push = OrderedDict({'text': item})

            text.append(push)

        elif item.name == 'span':
            content = item.get_text()
            if '文章網址' in content or '發信站' in content:
                continue
            push = OrderedDict({'text': content})

            text.append(push)

        elif item.name == 'a':
            img = item.get_text()
            href = img

            # imgur url replaction,  http://imgur.com/R2sLGim
            m = re.search('http://imgur.com/(\w+)', img)
            if m:
                href = 'http://i.imgur.com/' + m.group(1) + '.jpg'

            html = "<a href='" + href + "'>"
            html += img
            html += "</a>"
            if 'imgur' in href and 'jpg' in href:
                html += "<img src='" + href + "' title='" + href + \
                        "' class='img-rounded img-responsive'>"

            push = OrderedDict({'text': html})
            text.append(push)

        elif item['class'] == ['article-metaline-right']:
            continue

        elif item['class'] == ['article-metaline']:
            tag = item.span.get_text()
            value = item.span.next_sibling.get_text()
            post.update({tag: value})

        elif item['class'] == ['push']:
            push_tag = item.find('span', {"class": "push-tag"}).get_text()
            push_userid = item.find('span', {"class": "push-userid"}).get_text()
            push_content = item.find('span', {"class": "push-content"}).get_text()
            push_time = item.find('span', {"class": "push-ipdatetime"}).get_text()

            m = re.search('http://imgur.com/(\w+)', push_content)
            if m:
                href = 'http://i.imgur.com/' + m.group(1) + '.jpg'
                html = "<img src='" + href + "' title='" + href + "' class='img-rounded img-responsive'>"
                push_content += html

            push = OrderedDict()
            push.update({'tag': push_tag})
            push.update({'user': push_userid})
            push.update({'text': push_content})
            push.update({'time': push_time})

            text.append(push)

    post.update({'text': text})

    return post


def parse_board(board, post='index.html'):
    addr = 'https://www.ptt.cc/bbs/' + board + '/' + post
    r = requests.get(addr)
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find('div', {"class": "r-list-container bbs-screen"})

    over18 = soup.find('div', {"class": "over18-notice"})
    if over18 is not None:
        formdata = {'yes': 'yes'}
        # requests.post(addr, data=formdata, hooks=dict(response=parse_board(board)))
        requests.post(addr, data=formdata)
        return None

    articles = []
    for item in div.contents:
        if item == '\n':
            continue
        if item['class'] == ['r-list-sep']:
            break

        article = OrderedDict()
        title = item.find('div', {"class": "title"})
        href = title.a['href'] if title.a else None
        article.update({'title': title.get_text().strip()})
        article.update({'href': href})

        author = item.find('div', {"class": "author"})
        article.update({'author': author.get_text().strip()})

        date = item.find('div', {"class": "date"})
        article.update({'date': date.get_text().strip()})

        nrec = item.find('div', {"class": "nrec"})
        article.update({'nrec': nrec.get_text().strip()})

        mark = item.find('div', {"class": "mark"})
        article.update({'mark': mark.get_text().strip()})

        articles.insert(0, article)

    up = soup.find('div', {"class": "btn-group btn-group-paging"}).find_all('a')[1]['href']
    up = up.split('/')[-1]

    post = OrderedDict()
    post.update({'text': articles})
    post.update({'up': up})
    return post


def parse_hotboard():
    addr = 'https://www.ptt.cc/hotboard.html'
    r = requests.get(addr)
    content = r.content.decode('Big5-HKSCS', errors='backslashreplace')

    soup = BeautifulSoup(content, "html.parser")
    hotboard = soup.find_all('dd')

    nrec = 0
    name = ''
    title = ''
    boards = []

    for item in hotboard:
        td = item.table.tr.find_all('td')
        for i, col in enumerate(td):
            if i == 0:
                nrec = col.get_text()[3:]
            elif i == 1:
                name = col.get_text()
                href = col.a['href']
            elif i == 2:
                title = col.get_text()

        boards.append({'nrec': nrec, 'name': name, 'title': title, 'href':href})

    return boards

if __name__ == '__main__':
    # parse_board(addr)
    # LoL/M.1476714039.A.4CE.html
    # bbs/NBA/M.1476719760.A.438.html
    # Beauty/M.1476746586.A.D5C.html
    r = parse_post('Beauty', 'M.1476717114.A.BBD.html')
    # r = parse_board('Beauty')

    # for item in r:
    #     print(item)








