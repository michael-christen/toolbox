#!/usr/bin/env python
"""Get data from pocket export: https://getpocket.com/export
"""
import argparse
import csv
import datetime
import sys
from typing import List, NamedTuple

from bs4 import BeautifulSoup as BS


class Entry(NamedTuple):
    href: str
    title: str
    timestamp: int
    tags: List[str]
    is_read: bool


def main():
    parser = argparse.ArgumentParser(
        description='Read exported pocket html from stdin, output csv')
    parser.add_argument('--select', type=str,
                        choices=['all', 'read', 'unread'],
                        default='all')
    args = parser.parse_args()
    if args.select == 'unread':
        selector = lambda x: not x.is_read
    elif args.select == 'read':
        selector = lambda x: x.is_read
    else:
        selector = lambda x: True

    html = sys.stdin.read()
    parsed = BS(html, 'html.parser')
    lists = parsed.find_all('ul')
    assert len(lists) == 2
    # 0 = unread, 1 = read
    entries = []
    for is_read, l in zip([False, True], lists):
        for link in l.find_all('a'):
            attrs = link.attrs
            entries.append(Entry(
                href=link.attrs['href'],
                title=link.text,
                timestamp=int(link.attrs['time_added']),
                tags=link.attrs['tags'].split(',') if link.attrs['tags'] else [],
                is_read=is_read,
            ))
    fields = ['Name', 'URL', 'Tags', 'Timestamp', 'Done']
    writer = csv.DictWriter(sys.stdout, fields)
    writer.writeheader()
    for entry in filter(selector, entries):
        writer.writerow({
            'Name': entry.title,
            'URL': entry.href,
            'Tags': ','.join(entry.tags),
            'Timestamp': entry.timestamp,
            'Done': entry.is_read,
        })


if __name__ == '__main__':
    main()

