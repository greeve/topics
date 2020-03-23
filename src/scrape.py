# from models import Source, Term, Reference

import collections
import csv
import string

import requests

import utils

SOURCES = 'sources.csv'
ALPHA = string.ascii_lowercase
LANG = 'eng'
FILEPATH_TERMS = 'terms.csv'


def download_page(url):
    try:
        response = requests.get(url)
    except Exception as e:
        raise(e)

    if response.ok:
        return(response)
    else:
        response.raise_for_status()


def create_urls(source):
    if source.params:
        for letter in ALPHA:
            yield source.url + source.params.format(letter)
    else:
        yield source.url


def write_to_file(source, data, filename):
    with open(filename, 'a', encoding='utf-8') as fout:
        termwriter = csv.writer(fout, quotechar='"')
        for term_url, term in data:
            row = (source.slug, term, term_url)
            termwriter.writerow(row)


def gather_data(source):
    urls = list(create_urls(source))
    print(source)

    for url in urls:
        response = download_page(url)
        soup = utils.make_soup(response)

        try:
            terms = list(utils.SOURCE_SLUGS.get(source.slug)(soup))
        except Exception:
            print(soup)
            raise

        try:
            write_to_file(source, terms, FILEPATH_TERMS)
        except Exception:
            continue


def save_html(source):
    response = download_page(source.url)
    filename = '{}.html'.format(source.slug)
    with open(filename, 'wb') as fout:
        fout.write(response.content)


def main():
    # Write the output file with a heading row
    with open(FILEPATH_TERMS, 'w', encoding='utf-8') as fout:
        termwriter = csv.writer(fout, quotechar='"')
        termwriter.writerow(['source', 'term', 'url'])

    with open(SOURCES) as fin:
        reader = csv.DictReader(fin, dialect='unix')
        Source = collections.namedtuple('Source', reader.fieldnames)
        for row in reader:
            gather_data(Source(**row))


if __name__ == "__main__":
    main()
