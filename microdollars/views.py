from django.shortcuts import render
from django.views.generic import CreateView
from .models import Donation, OrganizationModel, Search
from .tables import DonationTable
from django.contrib.auth.models import User
from microdollars.forms import DonationForm, SearchForm, Search
from django.core.exceptions import ObjectDoesNotExist
from django_tables2.config import RequestConfig
from collections import Counter
# Create your views here.


def index(request):
    form = DonationForm(request.POST or None)
    if form.is_valid():
        tempForm = form.save(commit=False)
        if request.user and not request.user.is_anonymous:
            tempForm.user = request.user
        else:
            tempForm.user = None
        tempForm.save()
    context = {
        'form': form,
        'donation_list': Donation.objects,
        'organizations': OrganizationModel.objects.all(),
    }
    return render(request, "microdollars/index.html", context)


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
                orgName, 0) + float(donation.amount)
        return orgToTotalDonations

    if form.is_valid():
        username = form.cleaned_data['user_search']
        donationTable = DonationTable(usernameToUserDonations(username))
        RequestConfig(request).configure(donationTable)
        orgToTotalDonations = calcDonationsPerOrg(username)
        data = list(orgToTotalDonations.values())
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

    def getAllDonations():
        userList = User.objects.all()
        sum = 0
        leaderboard = []
        for user in userList:
            getUserDonations = usernameToUserDonations(user.username)
            for donation in getUserDonations:
                sum += donation.amount
            leaderboard.append((user.username, sum))
            sum = 0
        return leaderboard

    def sortThis():
        return sorted(getAllDonations(), key=lambda x: x[1], reverse=True)

    context = {
        'leaderboard': sortThis(),
    }

    return render(request, "microdollars/leaderboard.html", context)


def about(request):
    return render(request, "microdollars/about.html")
