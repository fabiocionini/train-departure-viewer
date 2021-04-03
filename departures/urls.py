from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'stations', views.StationViewSet)
router.register(r'departures', views.DepartureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
