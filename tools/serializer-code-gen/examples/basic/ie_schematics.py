from schematics.models import Model
from schematics.types import StringType, URLType


class Person(Model):
    name = StringType(required=True)
    website = URLType()
