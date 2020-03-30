#!/usr/bin/env python
import argparse
import collections
import csv
import logging
import pathlib

import utils


logger = logging.getLogger(__name__)

FILEPATH_TOPICS = 'bin/terms.csv'


def harvest_data(source, html):
    print(source.slug)
    p = pathlib.Path(html)
    source_path = p / source.slug
    source_paths = sorted(list(source_path.iterdir()))
    for f in source_paths:
        soup = utils.make_soup_from_file(f)

        try:
            topics = list(utils.SOURCE_SLUGS.get(source.slug)(soup))
            append_to_file(source, topics, FILEPATH_TOPICS)
        except Exception:
            print(soup)
            raise


def append_to_file(source, data, filename):
    with open(filename, 'a', encoding='utf-8') as fout:
        termwriter = csv.writer(fout, quotechar='"')
        for term_url, term in data:
            row = (source.slug, term, term_url)
            termwriter.writerow(row)


def get_argument_parser():
    parser = argparse.ArgumentParser(
        prog='harvest_topics',
        description='Harvest LDS Topics',
    )
    parser.add_argument(
        'sources',
        help='Filepath to sources csv file',
    )
    parser.add_argument(
        'html',
        help='Filepath to folder with downloaded html files',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
    )

    return parser


def main():
    """
    python src/harvest_topics.py src/sources.csv bin/sources
    """

    # Setup command line arguments
    parser = get_argument_parser()

    # Parse command line arguments and config file
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    with open(FILEPATH_TOPICS, 'w', encoding='utf-8') as fout:
        termwriter = csv.writer(fout, quotechar='"')
        termwriter.writerow(['source', 'term', 'url'])

    with open(args.sources) as fin:
        reader = csv.DictReader(fin, dialect='unix')
        Source = collections.namedtuple('Source', reader.fieldnames)
        for row in reader:
            harvest_data(Source(**row), args.html)


if __name__ == '__main__':
    main()
