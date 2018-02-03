# motd (Message of the day)

Generate motd files based on a .ini file.  For more information on motd see the
[docs](https://wiki.debian.org/motd).

This script should be able to turn

```ini

[service-1]
list tasks="service_1.sh --list"
delete tasks=service_1.sh --rm Capital

[another Service]
log location=/var/log/another_one

[empty service]
```

into this:

```sh
  _____            _                 _
  / ____|          | |     /\        | |
 | |     ___   ___ | |    /  \   _ __| |_
 | |    / _ \ / _ \| |   / /\ \ | '__| __|
 | |___| (_) | (_) | |  / ____ \| |  | |_
  \_____\___/ \___/|_| /_/    \_\_|   \__|

another service:
   ➢ log location: /var/log/another_one

service-1:
   ➢ list tasks:   "service_1.sh --list"
   ➢ delete tasks: service_1.sh --rm Capital

```

## Details

Look for header in /etc/pymotd/header

## Options

- `--config`: File that has `.ini` data. Defaults to `/etc/pymotd/config.ini`
- `--header`: File that contains the header, defaults to looking in
/etc/pymotd/header. If nothing present, doesn't display anything.
- `--arrow`: Character to separate tasks, defaults to `➢`.
- `--gen-motd`: Output in a format that would work for a motd file.

## Requirements

- Align all values vertically.
- Sort sections to get consistent output

## Gotchas

- Headers don't preserve case
