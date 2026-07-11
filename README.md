# 🌤️ ამინდის პროგნოზის აპლიკაცია (Django)

პირადი favorite ლოკაციების მართვა, მიმდინარე ამინდი + 5-დღიანი პროგნოზი
(OpenWeatherMap), ლოკაციების შედარება და **სტატისტიკური ანომალიის დეტექცია**
(rolling mean + std-dev → z-score) ისტორიულ მონაცემებზე დაყრდნობით.

## ფუნქციები
- რეგისტრაცია / login / temp_unit (°C/°F) preference
- Favorite ლოკაციების CRUD
- მიმდინარე ამინდი + 5-დღიანი პროგნოზი (30-წუთიანი cache)
- ლოკაციების comparison (გვერდიგვერდ)
- **Signature feature:** Z-score ანომალიის დეტექცია (threshold: ±2σ)
- REST API (DRF, ViewSet + Router)
- Django Admin (list_display, search_fields, list_filter, inline)

## Tech Stack
Django 5.x · Django REST Framework · SQLite · Bootstrap 5 · OpenWeatherMap API

---

## Project Structure

```
weather_forecast/
├── config/
│   ├── settings/{base,dev,prod}.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/       # Custom User, auth
│   ├── weather/         # domain app: models, views, forms, services, mixins
│   │   ├── services/    # WeatherService (გარე API), AnomalyDetectionService
│   │   ├── managers.py  # custom Manager/QuerySet
│   │   └── mixins.py    # custom CBV mixins
│   └── api/              # DRF: serializers, ViewSet+Router, permissions
├── templates/
├── static/
├── tests/
├── .env.example
├── requirements.txt
└── manage.py
```

---

## ლოკალური გაშვება

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# .env-ში ჩაწერეთ თქვენი OPENWEATHER_API_KEY
# (რეგისტრაცია: https://openweathermap.org/api — უფასო tier, 60 req/წთ)

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

საიტი ხელმისაწვდომი იქნება: `http://127.0.0.1:8000/`
ადმინ პანელი: `http://127.0.0.1:8000/admin/`

### ტესტების გაშვება
```bash
python manage.py test
```

### Anomaly Detection-ის დემო-მონაცემები
```bash
python manage.py seed_weather_logs --location-id=1 --days=30
```

---

## REST API Endpoints

| Method | URL | აღწერა |
|---|---|---|
| GET/POST | `/api/locations/` | ლოკაციების სია / შექმნა |
| GET/PUT/PATCH/DELETE | `/api/locations/<id>/` | ერთი ლოკაციის დეტალი/რედაქტირება/წაშლა |
| GET | `/api/weather/<city>/` | კონკრეტული ქალაქის მიმდინარე ამინდი |
| GET | `/api/forecast/<city>/` | 5-დღიანი პროგნოზი |
| GET | `/api/weather/compare/?locations=1,2` | რამდენიმე ლოკაციის შედარება + anomaly სტატუსი |

**DRF Pattern:** ViewSet + Router (`rest_framework.routers.DefaultRouter`) — `apps/api/urls.py`

---

## Deployment (PythonAnywhere)

- [ ] Web App → **Manual configuration**, Python 3.12
- [ ] `mkvirtualenv` + `pip install -r requirements.txt`
- [ ] `.env` ფაილი — `SECRET_KEY`, `OPENWEATHER_API_KEY`, `DEBUG=False`, `ALLOWED_HOST`
- [ ] WSGI ფაილში ჩასვით `config/wsgi.py`-ის შემცველობა + `sys.path.append('/home/username/weather_forecast')`
- [ ] `python manage.py migrate`
- [ ] `python manage.py collectstatic --noinput`
- [ ] `python manage.py createsuperuser`
- [ ] Static files mapping: `/static/` → `/home/username/weather_forecast/staticfiles`
- [ ] Settings module production-ისთვის: `config.settings.prod`

**Live URL:** _(დაამატეთ დეპლოის შემდეგ)_
**Admin URL:** `<live-url>/admin/`

---

## Signature Feature: Statistical Anomaly Detection

`apps/weather/services/anomaly_service.py` — ბოლო N დღის `WeatherLog.max_temp`
მონაცემებზე დაყრდნობით (`statistics.mean`, `statistics.stdev`) ითვლის:

```
z = (x - μ) / σ
```

სადაც `x` — დღევანდელი ტემპერატურა, `μ` — საშუალო, `σ` — სტანდარტული გადახრა.
`|z| >= threshold` (2σ) → ანომალიად აღინიშნება.

---

## Checklist შესაბამისობა

| მოთხოვნა | სად |
|---|---|
| 3+ app | `apps/accounts`, `apps/weather`, `apps/api` |
| 3+ model, 1+ FK | `Location(FK→User)`, `WeatherCache(FK→Location)`, `WeatherLog(FK→Location)` |
| Custom User | `apps/accounts/models.py` |
| 2 custom mixin | `OwnerQuerysetMixin`, `OwnerRequiredMixin` (`apps/weather/mixins.py`) |
| generic view override | `LocationListView.get_queryset()` |
| 2 Service Layer class | `WeatherService`, `AnomalyDetectionService` |
| custom Manager/QuerySet | `LocationManager`/`LocationQuerySet` |
| custom template filter | `to_unit` (`weather_extras.py`) |
| clean_<field>() | `LocationForm.clean_city_name`, `RegisterForm.clean_email` |
| Pagination + search | `LocationListView` (`paginate_by=10`, `Q objects`) |
| custom 404/500 | `templates/404.html`, `templates/500.html` |
