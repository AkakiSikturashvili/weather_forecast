"""
გაშვება: python manage.py test tests.test_anomaly_service
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.weather.models import Location, WeatherLog
from apps.weather.services import AnomalyDetectionService

User = get_user_model()


class AnomalyDetectionServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.location = Location.objects.create(user=self.user, city_name='Tbilisi', country='GE')
        today = timezone.localdate()
        # სტაბილური ისტორია: max_temp ყოველთვის ~20°C-ის ირგვლივ
        for i in range(10):
            WeatherLog.objects.create(
                location=self.location,
                date=today - timedelta(days=i),
                min_temp=15.0,
                max_temp=20.0 + (i % 2),  # 20 ან 21
            )

    def test_normal_temperature_is_not_anomaly(self):
        service = AnomalyDetectionService(threshold=2.0)
        result = service.detect(self.location, current_temp=20.5)
        self.assertFalse(result.is_anomaly)

    def test_extreme_temperature_is_anomaly(self):
        service = AnomalyDetectionService(threshold=2.0)
        result = service.detect(self.location, current_temp=45.0)
        self.assertTrue(result.is_anomaly)

    def test_insufficient_history_returns_no_anomaly(self):
        Location.objects.all().delete()
        empty_location = Location.objects.create(user=self.user, city_name='Batumi', country='GE')
        service = AnomalyDetectionService(threshold=2.0)
        result = service.detect(empty_location, current_temp=20.0)
        self.assertFalse(result.is_anomaly)
        self.assertIsNone(result.z_score)
