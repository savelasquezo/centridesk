from rest_framework import serializers

from api.models.token.my_token import MyToken


class MyTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyToken
        fields = ('name', 'key')
