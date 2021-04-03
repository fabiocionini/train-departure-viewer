from django.shortcuts import render

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from .models import Station, Departure
from .renderers import DeparturesAPIRenderer
from .serializers import StationSerializer, DepartureSerializer
from .versioning import DeparturesAPIVersioning


class StationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stations to be viewed.
    """
    renderer_classes = [DeparturesAPIRenderer]
    versioning_class = DeparturesAPIVersioning
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class DepartureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows departures to be viewed.
    """
    renderer_classes = [DeparturesAPIRenderer]
    versioning_class = DeparturesAPIVersioning
    queryset = Departure.objects.all().order_by('planned_time')
    serializer_class = DepartureSerializer
    # permission_classes = [permissions.IsAuthenticated]
