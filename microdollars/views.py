from django.shortcuts import render
from django.views.generic import CreateView
from .models import Donation

from microdollars.forms import DonationForm

# Create your views here.

def index(request):
    form = DonationForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'donation_list': Donation.objects,
    }
    return render(request, "microdollars/index.html", context)
