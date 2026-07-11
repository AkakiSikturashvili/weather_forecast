from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerQuerysetMixin(LoginRequiredMixin):
    """
    Custom mixin #1 — ავტომატურად ფილტრავს queryset-ს request.user-ის
    მიხედვით, რომ ერთმა მომხმარებელმა ვერ ნახოს სხვის ლოკაციები/მონაცემები.
    გამოიყენება ListView/DetailView-ებში.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class OwnerRequiredMixin(LoginRequiredMixin):
    """
    Custom mixin #2 — obj-level დაცვა DetailView/DeleteView/UpdateView-ებისთვის:
    თუ ობიექტი არ ეკუთვნის მოთხოვნის ავტორს, აგდებს PermissionDenied-ს (403).
    """

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user_id != self.request.user.id:
            raise PermissionDenied('ეს ლოკაცია არ გეკუთვნით.')
        return obj


class TempUnitContextMixin:
    """
    დამატებითი mixin — context-ში ამატებს მომხმარებლის სასურველ ტემპერატურის
    ერთეულს (°C/°F), template-ებში toggle-ისთვის გამოსაყენებლად.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['temp_unit'] = getattr(user, 'temp_unit', 'C') if user.is_authenticated else 'C'
        return context
