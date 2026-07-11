from django.conf import settings
from django.db import models

from .managers import LocationManager


class Location(models.Model):
    """
    მომხმარებლის favorite ლოკაცია.
    FK → User (one-to-many: ერთ user-ს შეიძლება ჰქონდეს რამდენიმე Location).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='locations',
    )
    city_name = models.CharField(max_length=120)
    country = models.CharField(max_length=80, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    is_home = models.BooleanField(default=False, verbose_name='საშინაო ლოკაცია')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = LocationManager()

    class Meta:
        ordering = ['-is_home', 'city_name']
        unique_together = ('user', 'city_name', 'country')

    def __str__(self):
        return f'{self.city_name}, {self.country}' if self.country else self.city_name


class WeatherCache(models.Model):
    """
    ბოლო მოთხოვნილი ამინდის cache — TTL (WEATHER_CACHE_TTL_MINUTES) გასვლის
    შემდეგ service layer ხელახლა მოიწვევს გარე API-ს.
    """
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='cache_entries'
    )
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    description = models.CharField(max_length=200)
    cached_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-cached_at']

    def __str__(self):
        return f'{self.location} @ {self.cached_at:%Y-%m-%d %H:%M}'


class WeatherLog(models.Model):
    """
    დღიური ამინდის ისტორია — გამოიყენება Anomaly Detection-ის
    (rolling mean + std-dev → z-score) სტატისტიკური ბაზისისთვის.
    """
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='logs'
    )
    date = models.DateField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()

    class Meta:
        ordering = ['-date']
        unique_together = ('location', 'date')

    def __str__(self):
        return f'{self.location} — {self.date} ({self.min_temp}–{self.max_temp}°C)'
