from django.shortcuts import render
from django.views.generic import CreateView
from .models import Donation, OrganizationModel, Search
from django.contrib.auth.models import User
from microdollars.forms import ProfileForm, DonationForm, SearchForm, Search
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.contrib.auth.models import User

def index(request):
    form = DonationForm(request.POST or None)
    message = ""
    if form.is_valid():
        tempForm = form.save(commit=False)
        if request.user and not request.user.is_anonymous:
            tempForm.user = request.user
        else:
            tempForm.user = None
        tempForm.save()
        message = '<div class="alert alert-success" role="alert">Successfully updated profile!</div>'
    context = {
        'form': form,
        'donation_list': Donation.objects,
        'organizations': OrganizationModel.objects.all(),
        'message': message,
    }
    return render(request, "microdollars/index.html", context)

def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    message = ""
    if form.is_valid():
        form.save()
        message = '<div class="alert alert-success" role="alert">Successfully updated profile!</div>'
    context = {
        'form': form,
        'message': message,
    }
    return render(request, "microdollars/profile.html", context)

def lookup(request):
    print("form")
    form = SearchForm(request.POST or None)
    donations = None

    def usernameToUserDonations(username):
        try:
            uid = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        return Donation.objects.filter(user=uid)
    if form.is_valid():
        username = form.cleaned_data['user_search']
        donations = usernameToUserDonations(username)

    context = {
        'form': form,
        'donation_list_search': donations,
    }

    return render(request, "microdollars/lookup.html", context)


def gamify(request):
    print("form")
    # form = SearchForm(request.POST or None)
    donations = None

    def usernameToUserDonations(username):
        try:
            uid = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        return Donation.objects.filter(user=uid)
    def exponential(user, donation):
        if(donation == 0):
            return (user, donation, 128578)
        elif(donation < 10):
            return (user, donation, 128513)
        elif(donation < 100):
            return (user, donation, 129297)
        elif(donation < 1000):
            return (user, donation, 129321)
        else:
            return (user, donation, 129332)
    def getAllDonations():
        userList = User.objects.all()
        sum = 0
        leaderboard = []
        for user in userList:
            getUserDonations = usernameToUserDonations(user.username)
            for donation in getUserDonations:
                sum += donation.amount
                # user = user.split("  /")
            leaderboard.append(exponential(user.username.capitalize(), sum))
            sum = 0
        return leaderboard

    def sortThis():
        return sorted(getAllDonations(), key=lambda x: x[1], reverse=True)

    # if form.is_valid():
    #     # username = form.cleaned_data['user_search']
    #     donations = getAllDonations()
    #     for i in donations:
    #         print(i)

    context = {
        # 'form': form,
        'leaderboard': sortThis(),
    }

    return render(request, "microdollars/leaderboard.html", context)


def about(request):
    return render(request, "microdollars/about.html")
