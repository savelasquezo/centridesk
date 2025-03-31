from abc import ABC
from base64 import b64decode
from json import loads

from rest_framework import serializers


class B64DecodeText(serializers.Field, ABC):
    def to_representation(self, value):
        return loads(b64decode(value).decode('utf-8'))
