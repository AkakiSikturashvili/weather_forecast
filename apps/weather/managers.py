from django.db import models
from django.db.models import Q


class LocationQuerySet(models.QuerySet):
    """
    Custom QuerySet/Manager — checklist-ის "მინ. 1 custom Manager/QuerySet"
    მოთხოვნისთვის.
    """

    def for_user(self, user):
        return self.filter(user=user)

    def home(self):
        return self.filter(is_home=True)

    def search(self, term):
        """გამოიყენება ძებნისთვის (Q objects) — city_name ან country მიხედვით."""
        if not term:
            return self
        return self.filter(
            Q(city_name__icontains=term) | Q(country__icontains=term)
        )


class LocationManager(models.Manager):
    def get_queryset(self):
        return LocationQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def home(self):
        return self.get_queryset().home()

    def search(self, term):
        return self.get_queryset().search(term)
