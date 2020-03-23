import string

from bs4 import BeautifulSoup

ALPHA = string.ascii_lowercase
URL_HYMNS = 'https://www.lds.org/music/index/hymns/topic?lang=eng'
URL_EOM = 'https://eom.byu.edu'


def create_urls(source):
    if source.params:
        for letter in ALPHA:
            yield source.url + source.params.format(letter)
    else:
        yield source.url


def make_soup(response):
    return BeautifulSoup(response.text, 'html.parser')


def scrape_bd(soup):
    for index, item in enumerate(soup.find(id='primary').find_all('ul', class_='topics guide')[0].children):  # noqa
        yield (item.a['href'], item.a.text)


def scrape_eom(soup):
    try:
        for index, item in enumerate(soup.find(id='mw-pages').find_all('li')):
            yield ('{}{}'.format(URL_EOM, item.a['href']), item.a.text)
    except Exception:
        yield


def scrape_gctopics(soup):
    for index, div in enumerate(soup.find_all('div')):
        if 'lumen-tile__title' in div.get('class', []):
            yield (div.a.get('href'), div.a.text.strip().split(' (')[0])


def scrape_gs(soup):
    for ul in soup.find(id='primary').find_all('ul'):
        if ['topics', 'guide'] == ul.get('class', []):
            for index, li in enumerate(ul.find_all('li')):
                yield (li.a.get('href'), li.a.text)


def scrape_hymntopics(soup):
    for div in soup.find_all('div'):
        if ['index-content-list'] == div.get('class', []):
            for index, h3 in enumerate(div.find_all('h3')):
                term = h3.text.strip().split(' (See')[0]
                yield ('{}#{}'.format(URL_HYMNS, h3.get('id')), term)


def scrape_tg(soup):
    for ul in soup.find(id='primary').find_all('ul'):
        if ['topics', 'guide'] == ul.get('class', []):
            for index, li in enumerate(ul.find_all('li')):
                yield (li.a.get('href'), li.a.text)


def scrape_topics(soup):
    for div in soup.find_all('div'):
        if ['topic-index__full'] == div.get('class', []):
            for index, li in enumerate(div.find_all('li')):
                yield (li.a.get('href'), li.a.text)


def scrape_tripleindex(soup):
    for ul in soup.find(id='primary').find_all('ul'):
        if ['topics', 'guide'] == ul.get('class', []):
            for index, li in enumerate(ul.find_all('li')):
                yield (li.a.get('href'), li.a.text)


def scrape_truetothefaith(soup):
    for tr in soup.find(id='primary').find_all('table')[0].find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            td = tds[1]
            if td.a and 'Message from the First Presidency' not in td.a.text:
                yield (td.a['href'], td.a.text)


SOURCE_SLUGS = {
    'gs': scrape_gs,
    'triple-index': scrape_tripleindex,
    'tg': scrape_tg,
    'bd': scrape_bd,
    'topics': scrape_topics,
    'gc-topics': scrape_gctopics,
    'true-to-the-faith': scrape_truetothefaith,
    'eom': scrape_eom,
    'hymn-by-topic': scrape_hymntopics,
}

