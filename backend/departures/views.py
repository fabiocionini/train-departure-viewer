from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey

from rest_framework.response import Response

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
    permission_classes = [HasAPIKey & IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        model, created = Station.objects.update_or_create(name=request.data['name'],
                                                          defaults={
                                                             'code': request.data['code']
                                                          })

        serializer = StationSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()

        if created:
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_200_OK)


class DepartureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows departures to be viewed.
    """
    renderer_classes = [DeparturesAPIRenderer]
    versioning_class = DeparturesAPIVersioning
    queryset = Departure.objects.all().order_by('planned_time')
    serializer_class = DepartureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        model, created = Departure.objects.update_or_create(name=request.data['name'],
                                                            defaults={
                                                                'station': Station.objects.get(id=request.data['station']),
                                                                'planned_time': request.data['planned_time'],
                                                                'direction': request.data['direction'],
                                                                'platform': request.data['platform'],
                                                                'train_type': request.data['train_type'],
                                                            })

        serializer = DepartureSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()

        if created:
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_200_OK)