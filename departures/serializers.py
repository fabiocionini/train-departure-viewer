from .models import Station, Departure
from rest_framework import serializers


class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
        fields = ['name', 'code']


class DepartureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Departure
        fields = ['station', 'planned_time', 'direction', 'platform', 'train_type']
