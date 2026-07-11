from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class RegisterForm(UserCreationForm):
    """
    რეგისტრაციის ფორმა — custom clean_email() ვალიდაციით
    (მოთხოვნილია checklist-ის "custom clean_<field>() ვალიდაცია").
    """

    email = forms.EmailField(required=True, label='ელ-ფოსტა')
    temp_unit = forms.ChoiceField(
        choices=CustomUser.TempUnit.choices,
        initial=CustomUser.TempUnit.CELSIUS,
        label='სასურველი ერთეული',
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'temp_unit', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'ამ ელ-ფოსტით მომხმარებელი უკვე რეგისტრირებულია.'
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if len(username) < 3:
            raise forms.ValidationError(
                'მომხმარებლის სახელი უნდა შეიცავდეს მინიმუმ 3 სიმბოლოს.'
            )
        return username
