from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LocationViewSet,
    CityWeatherAPIView,
    CityForecastAPIView,
    WeatherCompareAPIView,
)

router = DefaultRouter()
router.register('locations', LocationViewSet, basename='location')

urlpatterns = [
    path('', include(router.urls)),
    path('weather/compare/', WeatherCompareAPIView.as_view(), name='weather-compare'),
    path('weather/<str:city>/', CityWeatherAPIView.as_view(), name='city-weather'),
    path('forecast/<str:city>/', CityForecastAPIView.as_view(), name='city-forecast'),
]
