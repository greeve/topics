from bs4 import BeautifulSoup
import requests

SOURCE_SLUGS = {
    'gs': '',
    'triple-index': '',
    'tg': '',
    'bd': 'scrape_bd',
    'topics': '',
    'gc-topics': '',
    'true-to-the-faith': '',
    'eom': '',
    'hymn-by-topic': '',
}

def scrape_data(response):
    return BeautifulSoup(response, 'html.parser')

def scrape_bd(soup):
    for index, item in enumerate(soup.find(id='primary').ul.find_all('li')):
        print(item.a['href'], item.a.text)

soup = BeautifulSoup(open('eom_a.html', 'r', encoding='utf8'), 'html.parser')
for index, item in enumerate(soup.find(id='mw-pages').find_all('li')):
    print(item.a['href'], item.a.text)

soup = BeautifulSoup(open('gc-topics.html', 'r', encoding='utf8'), 'html.parser')
for index, div in enumerate(soup.find_all('div')):
    if 'lumen-tile__title' in div.get('class', []):
        print(div.a.get('href'), div.a.text.strip().split(' (')[0])

CLASSES = ['topics', 'guide']

soup = BeautifulSoup(open('gs.html', 'r', encoding='utf8'), 'html.parser')
for ul in soup.find(id='primary').find_all('ul'):
    if CLASSES == ul.get('class', []):
        for index, li in enumerate(ul.find_all('li')):
            print(li.a.get('href'), li.a.text)

CLASSES = ['index-content-list']
URL = 'https://www.lds.org/music/index/hymns/topic?lang=eng'

soup = BeautifulSoup(open('hymn-by-topic.html', 'r', encoding='utf8'), 'html.parser')
for div in soup.find_all('div'):
    if CLASSES == div.get('class', []):
        for index, h3 in enumerate(div.find_all('h3')):
            print('{}#{}'.format(URL, h3.get('id')), h3.text.strip().split(' (See')[0])

CLASSES = ['topics', 'guide']

soup = BeautifulSoup(open('tg.html', 'r', encoding='utf8'), 'html.parser')
for ul in soup.find(id='primary').find_all('ul'):
    if CLASSES == ul.get('class', []):
        for index, li in enumerate(ul.find_all('li')):
            print(li.a.get('href'), li.a.text)


CLASSES = ['topic-index__full']

soup = BeautifulSoup(open('topics.html', 'r', encoding='utf8'), 'html.parser')
print(soup.body)

for div in soup.find_all('div'):
    if CLASSES == div.get('class', []):
        for index, li in enumerate(div.find_all('li')):
            print(li.a.get('href'), li.a.text)

URL = 'https://www.lds.org/scriptures/triple-index?lang=eng&letter=a'
FILENAME = 'triple-index-a.html'

# r = requests.get(URL)
# with open(FILENAME, 'wb') as fout:
#     fout.write(r.content)


CLASSES = ['topics', 'guide']

soup = BeautifulSoup(open(FILENAME, 'r', encoding='utf8'), 'html.parser')
for ul in soup.find(id='primary').find_all('ul'):
    if CLASSES == ul.get('class', []):
        for index, li in enumerate(ul.find_all('li')):
            print(li.a.get('href'), li.a.text)

soup = BeautifulSoup(open('true-to-the-faith.html', 'r', encoding='utf8'), 'html.parser')
for tr in soup.find(id='primary').find_all('table')[0].find_all('tr'):
    tds = tr.find_all('td')
    if len(tds) > 1:
        td = tds[1]
        if td.a and 'Message from the First Presidency' not in td.a.text:
            print(td.a['href'], td.a.text)
