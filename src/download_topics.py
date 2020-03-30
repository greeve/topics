#!/usr/bin/env python
import argparse
import collections
import csv
import logging
import pathlib

import requests

import utils


logger = logging.getLogger(__name__)


def download_page(url):
    try:
        response = requests.get(url)
    except Exception as e:
        raise(e)

    if response.ok:
        return(response)
    else:
        response.raise_for_status()


def download_data(source, output):
    print(source)

    p = pathlib.Path(output)
    source_output = p / source.slug
    source_output.mkdir(parents=True, exist_ok=True)

    urls = list(utils.create_urls(source))

    for url in urls:
        response = download_page(url)
        if source.slug == 'eom':
            filename = '{}.html'.format(url.split('/')[-1].split(':')[-1])
        elif source.slug == 'hymn-by-topic':
            filename = '{}.html'.format(url.split('/')[-1].split('?')[0])
        else:
            filename = '{}.html'.format(source.slug)
        with open(source_output / filename, 'wb') as fout:
            fout.write(response.content)


def get_argument_parser():
    parser = argparse.ArgumentParser(
        prog='download_topics',
        description='Download LDS Topics',
    )
    parser.add_argument(
        'sources',
        help='Filepath to sources csv file',
    )
    parser.add_argument(
        '-o',
        '--output',
        default='bin/sources',
        help='Output filepath for downloaded data',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
    )

    return parser


def main():
    # Setup command line arguments
    parser = get_argument_parser()

    # Parse command line arguments and config file
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    with open(args.sources) as fin:
        reader = csv.DictReader(fin, dialect='unix')
        Source = collections.namedtuple('Source', reader.fieldnames)
        for row in reader:
            download_data(Source(**row), args.output)


if __name__ == '__main__':
    main()
