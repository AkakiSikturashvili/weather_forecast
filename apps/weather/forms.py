from django import forms

from .models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('city_name', 'country', 'is_home')
        widgets = {
           'city_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'მაგ. თბილისი'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'მაგ. GE'}),
            'is_home': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        """
        view-დან გადმოგვეცემა request.user, რომ clean()-ში შევძლოთ
        unique_together-ის წინასწარი შემოწმება (IntegrityError-მდე).
        """
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        city_name = cleaned_data.get('city_name')
        country = cleaned_data.get('country', '')

        if self.user and city_name is not None:
            already_exists = Location.objects.filter(
                user=self.user, city_name=city_name, country=country
            ).exists()
            if already_exists:
                raise forms.ValidationError(
                    'ეს ლოკაცია უკვე დამატებული გაქვთ თქვენს სიაში.'
                )
        return cleaned_data

    def clean_city_name(self):
        """
        Custom clean_<field>() — ქალაქის სახელი მხოლოდ ასოებით/whitespace-ით,
        checklist-ის Forms მოთხოვნისთვის.
        """
        city_name = self.cleaned_data['city_name'].strip()
        if not city_name.replace(' ', '').replace('-', '').isalpha():
            raise forms.ValidationError(
                'ქალაქის სახელი უნდა შეიცავდეს მხოლოდ ასოებს.'
            )
        return city_name.title()