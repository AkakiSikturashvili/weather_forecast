from django.contrib import admin

from .models import Location, WeatherCache, WeatherLog


class WeatherLogInline(admin.TabularInline):
    """FK-ისთვის inline — checklist-ის "inline (FK-ისთვის)" მოთხოვნა."""
    model = WeatherLog
    extra = 1


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'country', 'user', 'is_home', 'created_at')
    list_filter = ('is_home', 'country')
    search_fields = ('city_name', 'country', 'user__username')
    inlines = [WeatherLogInline]


@admin.register(WeatherCache)
class WeatherCacheAdmin(admin.ModelAdmin):
    list_display = ('location', 'temperature', 'humidity', 'description', 'cached_at')
    list_filter = ('cached_at',)
    search_fields = ('location__city_name',)


@admin.register(WeatherLog)
class WeatherLogAdmin(admin.ModelAdmin):
    list_display = ('location', 'date', 'min_temp', 'max_temp')
    list_filter = ('date',)
    search_fields = ('location__city_name',)
