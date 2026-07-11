from django.urls import path

from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.LocationListView.as_view(), name='location-list'),
    path('locations/add/', views.LocationCreateView.as_view(), name='location-add'),
    path('locations/<int:pk>/', views.LocationDetailView.as_view(), name='location-detail'),
    path('locations/<int:pk>/delete/', views.LocationDeleteView.as_view(), name='location-delete'),
    path('compare/', views.LocationCompareView.as_view(), name='location-compare'),
]
