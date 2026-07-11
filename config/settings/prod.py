from .base import *  # noqa

DEBUG = False

# PythonAnywhere-ზე დეპლოისას შეცვალეთ თქვენი username-ით
ALLOWED_HOSTS = [env('ALLOWED_HOST', default='yourusername.pythonanywhere.com')]

# production-ში DEBUG=False-ის დროს Django ავტომატურად იყენებს
# templates/404.html და templates/500.html ფაილებს (თუ handler-ები
# root urls.py-ში მითითებულია — იხ. config/urls.py)
