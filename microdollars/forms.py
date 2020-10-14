from django import forms
from django.utils.translation import gettext_lazy

from microdollars.models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('donateto', 'amount', 'comment')

        widgets = {
            'donateto': forms.Select(choices = Donation.ORGANIZATION_CHOICES, attrs={'class': 'form-control donationitem'}),
            'amount': forms.TextInput(attrs={'class':'form-control donationitem'}),
            'comment': forms.TextInput(attrs={'class':'form-control donationitem'}),
        }

        labels = {
            'donateto': gettext_lazy('Donate to'),
            'amount': gettext_lazy('Amount'),
            'comment': gettext_lazy('Comment'),
        }
