from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('api/', include('apps.api.urls')),
    path('', include('apps.weather.urls', namespace='weather')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# --- custom error handlers (მოთხოვნილია checklist-ით) ---
# ეს მუშაობს მხოლოდ DEBUG=False-ის დროს (config/settings/prod.py)
handler404 = 'apps.weather.views.custom_404_view'
handler500 = 'apps.weather.views.custom_500_view'
