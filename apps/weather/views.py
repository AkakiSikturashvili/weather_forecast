from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, TemplateView

from .forms import LocationForm
from .mixins import OwnerQuerysetMixin, OwnerRequiredMixin, TempUnitContextMixin
from .models import Location
from .services import WeatherService, AnomalyDetectionService, WeatherAPIError


class LocationListView(OwnerQuerysetMixin, TempUnitContextMixin, ListView):
    """
    Generic ListView-ის override (get_queryset) — search + pagination.
    checklist: "მინ. 1 generic view override", "Paginator ... search + filter".
    """
    model = Location
    template_name = 'weather/location_list.html'
    context_object_name = 'locations'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()  # user-ით უკვე გაფილტრულია (OwnerQuerysetMixin)
        search_term = self.request.GET.get('q', '').strip()
        return queryset.search(search_term) if search_term else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('q', '')
        return context


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'weather/location_form.html'
    success_url = reverse_lazy('weather:location-list')

    def get_form_kwargs(self):
        """request.user გადავცემთ ფორმას — LocationForm.clean()-ს სჭირდება
        დუბლიკატის წინასწარი შემოწმებისთვის (IntegrityError-ის თავიდან ასაცილებლად)."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'"{form.instance.city_name}" დაემატა თქვენს ლოკაციებში.')
        return super().form_valid(form)


class LocationDeleteView(OwnerRequiredMixin, DeleteView):
    model = Location
    template_name = 'weather/location_confirm_delete.html'
    success_url = reverse_lazy('weather:location-list')


class LocationDetailView(OwnerRequiredMixin, TempUnitContextMixin, DetailView):
    """
    კონკრეტული ლოკაციის დეტალები — service layer-ის გამოძახებით
    (WeatherService — current+forecast, AnomalyDetectionService — z-score).
    """
    model = Location
    template_name = 'weather/location_detail.html'
    context_object_name = 'location'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.object
        weather_service = WeatherService()
        anomaly_service = AnomalyDetectionService()

        try:
            current = weather_service.get_current_weather(location)
            forecast = weather_service.get_forecast(location)
            anomaly = anomaly_service.detect(location, current.temperature)
            context['current'] = current
            context['forecast'] = forecast
            context['anomaly'] = anomaly
        except WeatherAPIError as exc:
            context['api_error'] = str(exc)

        return context


class LocationCompareView(LoginRequiredMixin, TempUnitContextMixin, TemplateView):
    """ორი ლოკაციის გვერდიგვერდ შედარება."""
    template_name = 'weather/location_compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_ids = self.request.GET.getlist('location')
        locations = Location.objects.for_user(self.request.user).filter(id__in=location_ids)

        weather_service = WeatherService()
        comparisons = []
        for location in locations:
            try:
                current = weather_service.get_current_weather(location)
                comparisons.append({'location': location, 'current': current})
            except WeatherAPIError:
                comparisons.append({'location': location, 'current': None})

        context['comparisons'] = comparisons
        context['all_locations'] = Location.objects.for_user(self.request.user)
        return context


# --- Custom error handlers (config/urls.py-ში handler404/handler500) ---

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)
