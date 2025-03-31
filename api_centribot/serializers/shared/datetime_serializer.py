from abc import ABC
from datetime import datetime

from rest_framework import serializers


class DateTimeFormat(serializers.Field, ABC):
    def to_representation(self, value):
        return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
