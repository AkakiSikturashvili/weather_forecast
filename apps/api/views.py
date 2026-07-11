"""
DRF Pattern: ViewSet + Router (კენტი student ID ვარიანტი).
`rest_framework.routers.DefaultRouter`-ით რეგისტრირებულია LocationViewSet
(იხ. apps/api/urls.py).
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.weather.models import Location
from apps.weather.services import WeatherService, AnomalyDetectionService, WeatherAPIError

from .permissions import IsOwner
from .serializers import LocationSerializer, WeatherCacheSerializer, AnomalySerializer


class LocationViewSet(viewsets.ModelViewSet):
    """
    /api/locations/         GET (list), POST (create)
    /api/locations/<id>/    GET, PUT, PATCH, DELETE
    """
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Location.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CityWeatherAPIView(APIView):
    """GET /api/weather/<city>/ — მოცემული ქალაქის მიმდინარე ამინდი."""
    permission_classes = [IsAuthenticated]

    def get(self, request, city):
        location, _ = Location.objects.get_or_create(
            user=request.user, city_name=city.title(), country='',
        )
        try:
            current = WeatherService().get_current_weather(location)
        except WeatherAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response(WeatherCacheSerializer(current).data)


class CityForecastAPIView(APIView):
    """GET /api/forecast/<city>/ — 5-დღიანი პროგნოზი."""
    permission_classes = [IsAuthenticated]

    def get(self, request, city):
        location, _ = Location.objects.get_or_create(
            user=request.user, city_name=city.title(), country='',
        )
        try:
            forecast = WeatherService().get_forecast(location)
        except WeatherAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response(forecast)


class WeatherCompareAPIView(APIView):
    """
    GET /api/weather/compare/?locations=1,2,3
    რამდენიმე ლოკაციის მიმდინარე ამინდის + anomaly-სტატუსის შედარება.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ids_param = request.query_params.get('locations', '')
        location_ids = [int(i) for i in ids_param.split(',') if i.strip().isdigit()]
        locations = Location.objects.for_user(request.user).filter(id__in=location_ids)

        weather_service = WeatherService()
        anomaly_service = AnomalyDetectionService()
        results = []
        for location in locations:
            try:
                current = weather_service.get_current_weather(location)
                anomaly = anomaly_service.detect(location, current.temperature)
                results.append({
                    'location': LocationSerializer(location).data,
                    'weather': WeatherCacheSerializer(current).data,
                    'anomaly': AnomalySerializer(anomaly.__dict__).data,
                })
            except WeatherAPIError as exc:
                results.append({
                    'location': LocationSerializer(location).data,
                    'error': str(exc),
                })

        return Response(results)
