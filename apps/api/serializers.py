from rest_framework import serializers

from apps.weather.models import Location, WeatherCache


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'city_name', 'country', 'lat', 'lon', 'is_home', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate_city_name(self, value):
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError('ქალაქის სახელი უნდა შეიცავდეს მხოლოდ ასოებს.')
        return value.title()


class WeatherCacheSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.city_name', read_only=True)

    class Meta:
        model = WeatherCache
        fields = (
            'id', 'location', 'location_name', 'temperature', 'feels_like',
            'humidity', 'wind_speed', 'description', 'cached_at',
        )


class AnomalySerializer(serializers.Serializer):
    is_anomaly = serializers.BooleanField()
    z_score = serializers.FloatField(allow_null=True)
    mean = serializers.FloatField(allow_null=True)
    std_dev = serializers.FloatField(allow_null=True)
    sample_size = serializers.IntegerField()
    threshold = serializers.FloatField()
