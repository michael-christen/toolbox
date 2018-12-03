#!/usr/bin/env python
"""Simple script to get IMDB id's through its API from trello cards with the
name of a movie.
"""
import json
import time
from imdb import IMDb

def main():
    with open('movies.json') as f:
        trello = json.load(f)
    names = [c['name'] for c in trello['cards']]
    name2id = {}
    ia = IMDb()
    with open('movies.csv', 'w') as f:
        f.write('imdbId\n')
        for i, name in enumerate(names):
            matches = ia.search_movie(name)
            if matches:
                imdbId = matches[0].getID()
                name2id[name] = 'tt{}'.format(imdbId)
                f.write('{}\n'.format(imdbId))
            else:
                print "No match for: {}".format(name)
            print "{}/{}".format(i, len(names))
            time.sleep(0.5)


if __name__ == '__main__':
    main()

