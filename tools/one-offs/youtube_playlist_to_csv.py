#!/usr/bin/env python3
import csv
import json
import sys


def main():
    rows = get_rows()
    write_rows(rows)


def write_rows(rows):
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=['video_id', 'image_url', 'title', 'description'])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)


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
        # TODO: Look for recipe url in description
        row = {
            'video_id': video_id,
            'image_url': image_url,
            'title': title,
            'description': description,
        }
        rows.append(row)
    return rows


if __name__ == '__main__':
    main()
