from marshmallow import Schema, fields


class Person(Schema):
    name = fields.Str()
    website = fields.URL()


""" Additional cases
- lists
- nested serialization
- custom validators
- custom fields
- various field options ie) max_length

The gateway is a union of all options, the various parsers/renderers merely
take a certain subset from that union.
"""
