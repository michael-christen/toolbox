#!/usr/bin/env python3
import csv
import json
import sys
import re

RECIPE_RE = re.compile(
    r'[Rr]ecipe( here)?: (?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%0-9a-fA-F][0-9a-fA-F]))+)')

def main():
    rows = get_rows()
    write_rows(rows)


def write_rows(rows):
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=['video_id', 'image_url', 'title', 'recipe_url', 'description'])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)


def get_recipe_url_from_description(description):
    match = RECIPE_RE.search(description)
    if not match:
        return ''
    else:
        return match.group('url')


def get_rows():
    data = json.load(sys.stdin)

    rows = []
    for item in data:
        video_id = item['contentDetails']['videoId']
        image_url = ''
        for res in ['maxres', 'high', 'standard', 'medium', 'default']:
            try:
                image_url = item['snippet']['thumbnails'][res]['url']
            except KeyError:
                pass
            else:
                break
        if not image_url:
            raise KeyError(f'No thumbnail found in {item}')
        title = item['snippet']['title']
        description = item['snippet']['description']
        recipe_url = get_recipe_url_from_description(description)
        row = {
            'video_id': video_id,
            'image_url': image_url,
            'title': title,
            'description': description,
            'recipe_url': recipe_url,
        }
        rows.append(row)
    return rows


if __name__ == '__main__':
    main()
