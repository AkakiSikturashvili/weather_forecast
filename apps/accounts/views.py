from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm


class RegisterView(CreateView):
    """
    რეგისტრაციის CBV — generic CreateView-ის override (form_valid),
    checklist-ის "მინ. 1 generic view override" მოთხოვნისთვის.
    """
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('weather:location-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # ავტომატური login რეგისტრაციის შემდეგ
        login(self.request, self.object)
        messages.success(
            self.request,
            f'კეთილი იყოს თქვენი მობრძანება, {self.object.username}!'
        )
        return response
