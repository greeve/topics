from models import Source, Term, Reference

import collections
import csv
import string

import requests
from bs4 import BeautifulSoup

SOURCES = 'sources.csv'
ALPHA = string.ascii_lowercase
LANG = 'eng'


def scrape_page(url):
    try:
        response = requests.get(url)
    except Exception as e:
        raise(e)

    if response.ok:
        return(response)
    else:
        response.raise_for_status()


def parse_alpha(response):
    pass


def parse_single(response):
    pass


def gather_data(source):
    if source.params:
        for letter in ALPHA:
            url = source.url + source.params.format(LANG, letter)
            response = scrape_page(url)
            parse_alpha(response)
    else:
        url = source.url
        response = scrape_page(url)
        parse_single(response)


def save_html(source):
    response = scrape_page(source.url)
    filename = '{}.html'.format(source.slug)
    with open(filename, 'wb') as fout:
        fout.write(response.content)

def main():
    with open(SOURCES) as fin:
        reader = csv.DictReader(fin, dialect='unix')
        Source = collections.namedtuple('Source', reader.fieldnames)
        for row in reader:
            # gather_data(Source(**row))
            save_html(Source(**row))

if __name__ == "__main__":
    main()

