from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'temp_unit', 'is_staff', 'date_joined')
    list_filter = ('temp_unit', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('დამატებითი პარამეტრები', {'fields': ('temp_unit',)}),
    )
