import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.weather.models import Location, WeatherLog


class Command(BaseCommand):
    help = 'ავსებს WeatherLog-ს სატესტო ისტორიული მონაცემებით (Anomaly Detection-ის დემოსთვის).'

    def add_arguments(self, parser):
        parser.add_argument('--location-id', type=int, required=True)
        parser.add_argument('--days', type=int, default=30)

    def handle(self, *args, **options):
        location = Location.objects.get(pk=options['location_id'])
        days = options['days']
        today = timezone.localdate()

        base_temp = random.uniform(15, 25)
        created = 0
        for i in range(days):
            date = today - timedelta(days=i)
            min_temp = base_temp - random.uniform(3, 6)
            max_temp = base_temp + random.uniform(2, 5)
            _, was_created = WeatherLog.objects.update_or_create(
                location=location,
                date=date,
                defaults={'min_temp': round(min_temp, 1), 'max_temp': round(max_temp, 1)},
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f'{location}-სთვის შეიქმნა/განახლდა {days} დღის ჩანაწერი ({created} ახალი).'
        ))
