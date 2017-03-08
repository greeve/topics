from models import Source, Term, Reference

import collections
import csv
import string

import requests
from bs4 import BeautifulSoup

from . import utils

SOURCES = 'sources.csv'
ALPHA = string.ascii_lowercase
LANG = 'eng'


def download_page(url):
    try:
        response = requests.get(url)
    except Exception as e:
        raise(e)

    if response.ok:
        return(response)
    else:
        response.raise_for_status()


def gather_data(source):
    if source.params:
        for letter in ALPHA:
            url = source.url + source.params.format(LANG, letter)
            response = download_page(url)
            soup = utils.make_soup(response)
            term_url, term = utils.get(source.slug)(soup)
    else:
        url = source.url
        response = download_page(url)
        soup = utils.make_soup(response)
        term_url, term = utils.get(source.slug)(soup)


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
            gather_data(Source(**row))

if __name__ == "__main__":
    main()

