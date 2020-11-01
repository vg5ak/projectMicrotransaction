from django.shortcuts import render
from django.views.generic import CreateView
from .models import Donation, OrganizationModel, Search
from django.contrib.auth.models import User
from microdollars.forms import DonationForm, SearchForm, Search
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def index(request):
    form = DonationForm(request.POST or None)
    if form.is_valid():
        tempForm = form.save(commit=False)
        tempForm.user = request.user
        tempForm.save() 
    context = {

        'form': form,
        'donation_list': Donation.objects,
        'organizations': OrganizationModel.objects.all(),
    }
    return render(request, "microdollars/index.html", context)




def lookup(request):
    print("form")
    form = SearchForm(request.POST or None)
    donations = None

    def usernameToUserDonations(username):
        try:
            uid = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        return Donation.objects.filter(user = uid)
    if form.is_valid():
        username = form.cleaned_data['user_search']
        print(username)
        donations = usernameToUserDonations(username)
    
    context = {
        'form': form,
        'donation_list_search': donations,
    }
    
    return render(request, "microdollars/lookup.html", context)


def about(request):
    return render(request, "microdollars/about.html")

