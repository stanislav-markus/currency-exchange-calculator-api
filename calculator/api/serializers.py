from django.contrib.auth.models import User, Group
from calculator.api.models import CurrencyRate, CurrencyPair
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CurrencyPairSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrencyPair
        fields = ['code']


class CurrencyRateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = ['rate', 'pair', 'date']
