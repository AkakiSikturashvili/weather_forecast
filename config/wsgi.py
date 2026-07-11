"""
WSGI config. PythonAnywhere-ზე ეს ფაილის შემცველობა უნდა ჩასვათ
"Web" ტაბის WSGI configuration file-ში (იხ. README.md → Deployment).
"""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
