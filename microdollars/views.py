from django.shortcuts import render
from django.views.generic import CreateView
from .models import Donation, OrganizationModel, Search
from .tables import DonationTable
from django.contrib.auth.models import User
from microdollars.forms import ProfileForm, DonationForm, SearchForm, Search
from django.core.exceptions import ObjectDoesNotExist
from django_tables2.config import RequestConfig
from collections import Counter
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
# Create your views here.


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
        messages.success(
            request, "Successfully completed transaction!")
        return redirect(reverse('index'))

    if request.user.is_anonymous:
        messages.warning(
            request, "You're not logged in, so your donation will be anonymous. It won't show up on leaderboards, or on any profile!")

    context = {
        'form': form,
        'donation_list': Donation.objects,
        'organizations': OrganizationModel.objects.all(),
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


def usernameToUserDonations(username):
    try:
        uid = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None
    return Donation.objects.filter(user=uid)


def lookup(request):
    print("form")
    form = SearchForm(request.GET or None)
    donationTable = None
    data = None
    labels = None

    def calcDonationsPerOrg(username):
        userDonations = usernameToUserDonations(username)
        orgToTotalDonations = dict()
        for donation in userDonations:
            orgName = donation.donateto.organization_name
            orgToTotalDonations[orgName] = orgToTotalDonations.get(
                orgName, 0) + donation.amount
        return orgToTotalDonations

    if form.is_valid():
        username = form.cleaned_data['user_search']
        donationTable = DonationTable(usernameToUserDonations(username))
        RequestConfig(request).configure(donationTable)
        orgToTotalDonations = calcDonationsPerOrg(username)
        data = [float(val)
                for val in list(orgToTotalDonations.values())]
        labels = list(orgToTotalDonations.keys())

    context = {
        'form': form,
        'donationTable': donationTable,
        'data': data,
        'labels': labels,
    }
    return render(request, "microdollars/lookup.html", context)


def gamify(request):
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
            return (user, donation, 128081)

    def getAllDonations():
        userList = User.objects.all()
        sum = 0
        leaderboard = []
        for user in userList:
            getUserDonations = usernameToUserDonations(user.username)
            for donation in getUserDonations:
                sum += donation.amount
            leaderboard.append(exponential(user.username.capitalize(), sum))
            sum = 0
        return leaderboard

    def sortThis():
        return sorted(getAllDonations(), key=lambda x: x[1], reverse=True)

    def numberList(rankingslist):
        finallist = []
        i = 1
        for rankings in rankingslist:
            finallist.append((i, rankings[0], rankings[1], rankings[2]))
            i += 1
        return finallist

    context = {
        'leaderboard': numberList(sortThis()),
    }

    return render(request, "microdollars/leaderboard.html", context)


def about(request):
    return render(request, "microdollars/about.html")
