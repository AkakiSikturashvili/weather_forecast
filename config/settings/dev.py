from .base import *  # noqa
import os
from pathlib import Path

# ვინაიდან ფაილი config/settings/ საქაღალდეშია, 3-ჯერ გვჭირდება .parent, რომ მთავარ დირექტორიაში გავიდეთ
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'weatherforecast.pythonanywhere.com']

# თუ base.py-ში TEMPLATES უკვე გიწერია, აქ მისი თავიდან აღწერა საერთოდ აღარ გჭირდება.
# მაგრამ თუ მაინც გინდა აქ გქონდეს, სწორი გზა არის:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]