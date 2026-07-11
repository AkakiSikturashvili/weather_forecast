"""
Service Layer #1 — გარე API (OpenWeatherMap) ინტეგრაცია + caching.
"""
from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone

from ..models import WeatherCache


class WeatherAPIError(Exception):
    """გარე API-სთან დაკავშირებული შეცდომებისთვის."""


class WeatherService:
    """
    პასუხისმგებელია OpenWeatherMap-იდან მიმდინარე ამინდის მიღებაზე,
    30-წუთიან cache-ზე (WeatherCache model) და unit-კონვერტაციაზე.
    """

    def __init__(self, session: requests.Session | None = None):
        self.session = session or requests.Session()
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.OPENWEATHER_BASE_URL
        self.ttl = timedelta(minutes=settings.WEATHER_CACHE_TTL_MINUTES)

    def get_current_weather(self, location, force_refresh: bool = False) -> WeatherCache:
        """
        აბრუნებს WeatherCache ჩანაწერს — ან ახალს, ან cache-ს, TTL-ის მიხედვით.
        """
        latest = location.cache_entries.order_by('-cached_at').first()
        is_fresh = latest and (timezone.now() - latest.cached_at) < self.ttl

        if is_fresh and not force_refresh:
            return latest

        data = self._fetch_from_api(location.city_name, location.country)
        return WeatherCache.objects.create(
            location=location,
            temperature=data['main']['temp'],
            feels_like=data['main']['feels_like'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
            description=data['weather'][0]['description'],
        )

    def get_forecast(self, location, days: int = 5) -> list[dict]:
        """5-დღიანი პროგნოზი (OpenWeatherMap /forecast endpoint, 3-სთ ინტერვალით)."""
        params = {
            'q': f'{location.city_name},{location.country}'.rstrip(','),
            'appid': self.api_key,
            'units': 'metric',
        }
        response = self.session.get(f'{self.base_url}/forecast', params=params, timeout=10)
        if response.status_code != 200:
            raise WeatherAPIError(f'OpenWeatherMap-ის შეცდომა: {response.status_code}')
        payload = response.json()
        # წუთამდე ვამარტივებთ — 1 ჩანაწერი დღეში (შუადღის მონაცემი)
        daily = [entry for entry in payload.get('list', []) if '12:00:00' in entry.get('dt_txt', '')]
        return daily[:days]

    def _fetch_from_api(self, city_name: str, country: str) -> dict:
        params = {
            'q': f'{city_name},{country}'.rstrip(','),
            'appid': self.api_key,
            'units': 'metric',
        }
        response = self.session.get(f'{self.base_url}/weather', params=params, timeout=10)
        if response.status_code != 200:
            raise WeatherAPIError(f'OpenWeatherMap-ის შეცდომა: {response.status_code}')
        return response.json()
