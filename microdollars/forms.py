from allauth.account.forms import LoginForm
from django import forms
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError

from microdollars.models import Donation, OrganizationModel, Search


class DonationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['donateto'].queryset = OrganizationModel.objects.all()
        self.fields['donateto'].empty_label = None

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data <= 0:
            raise ValidationError("You can't donate a non-positive amount!")
        return data

    class Meta:
        model = Donation
        fields = ('donateto', 'amount', 'comment')
        widgets = {
            'donateto': forms.Select(attrs={'class': 'form-control donationitem'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control donationitem'}),
            'comment': forms.TextInput(attrs={'class': 'form-control donationitem'}),
        }

        labels = {

            'donateto': gettext_lazy('Donate to'),
            'amount': gettext_lazy('Amount'),
            'comment': gettext_lazy('Comment'),

        }


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ('user_search',)
        widgets = {
            'user_search': forms.TextInput(attrs={'class': 'form-control donationitem'})
        }
        labels = {
            'user_search': gettext_lazy("Input a user's name ")
        }


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = OrganizationModel
        fields = ('organization_name', 'about_me')
        widgets = {
            'organization_name': forms.TextInput(attrs={'class': 'form-control donationitem'}),
            'about_me': forms.TextInput(attrs={'class': 'form-control donationitem'}),
        }
        labels = {
            'organization_name': gettext_lazy('Organization'),
            'about_me': gettext_lazy('About this Organization'),
        }
        # def __unicode__


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(
            attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})
