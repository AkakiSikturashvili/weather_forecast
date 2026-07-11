from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    გაფართოებული User მოდელი — checklist-ის თანახმად:
    "Custom User (AbstractUser)".
    """

    class TempUnit(models.TextChoices):
        CELSIUS = 'C', 'ცელსიუსი (°C)'
        FAHRENHEIT = 'F', 'ფარენჰეიტი (°F)'

    temp_unit = models.CharField(
        max_length=1,
        choices=TempUnit.choices,
        default=TempUnit.CELSIUS,
        help_text='მომხმარებლის სასურველი ტემპერატურის ერთეული',
    )

    def __str__(self):
        return self.username
