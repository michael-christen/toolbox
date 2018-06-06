from rest_framework import serializers


class Person(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    website = serializers.URLField()
