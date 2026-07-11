"""
გაშვება: python manage.py test tests.test_models
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.weather.models import Location

User = get_user_model()


class LocationManagerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass12345')
        self.user2 = User.objects.create_user(username='bob', password='pass12345')

        self.tbilisi = Location.objects.create(
            user=self.user1, city_name='Tbilisi', country='GE', is_home=True
        )
        self.batumi = Location.objects.create(
            user=self.user1, city_name='Batumi', country='GE'
        )
        self.paris = Location.objects.create(
            user=self.user2, city_name='Paris', country='FR'
        )

    def test_for_user_filters_correctly(self):
        qs = Location.objects.for_user(self.user1)
        self.assertEqual(qs.count(), 2)
        self.assertNotIn(self.paris, qs)

    def test_home_returns_only_home_locations(self):
        qs = Location.objects.home()
        self.assertEqual(list(qs), [self.tbilisi])

    def test_search_matches_city_or_country(self):
        qs = Location.objects.search('tbil')
        self.assertIn(self.tbilisi, qs)
        self.assertNotIn(self.batumi, qs)

    def test_str_representation(self):
        self.assertEqual(str(self.tbilisi), 'Tbilisi, GE')

    def test_unique_together_constraint(self):
        from django.db import IntegrityError, transaction
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Location.objects.create(user=self.user1, city_name='Tbilisi', country='GE')
