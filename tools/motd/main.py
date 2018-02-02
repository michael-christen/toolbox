#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser

from collections import defaultdict

def main():
    header_file = 'header'
    with open(header_file, 'r') as f:
        print f.read()
    config_file = 'config.ini'
    arrow = u'➢'
    config = configparser.ConfigParser()
    # Preserve case
    config.optionxform = str
    config.read(config_file)
    section2pairs = defaultdict(dict)
    max_key_length = 0
    for section in config.sections():
        for k, v in config.items(section):
            section2pairs[section][k] = v
            max_key_length = max(max_key_length, len(k))

    # TODO: Remove quotes
    f = u'   %s {:<%d} {}' % (arrow, max_key_length + 1)
    for section, pairs in section2pairs.items():
        print u'\n{}'.format(section)
        for k, v in pairs.items():
            print f.format(k + u':', v)


if __name__ == '__main__':
    main()
