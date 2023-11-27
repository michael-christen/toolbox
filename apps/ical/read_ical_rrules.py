#!/usr/bin/env python
import icalendar
import sys


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        raise Exception("Need to specify path to .ics file")
    with open(filename, 'r') as f:
        cal = icalendar.Calendar.from_ical(f.read())
    subcomponents = [s for s in cal.subcomponents if 'RRULE' in s]
    for s in subcomponents:
        rrule_str = ', '.join('{} -> {}'.format(k, v)
                             for k, v in sorted(s['RRULE'].items()))
        print '{}: {}'.format(s['SUMMARY'], rrule_str)


if __name__ == '__main__':
    main()
