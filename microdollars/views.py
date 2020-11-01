from django.shortcuts import render
from django.views.generic import CreateView
from .models import Donation, OrganizationModel
from microdollars.forms import DonationForm

# Create your views here.

def index(request):
    form = DonationForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'donation_list': Donation.objects,
        'organizations': OrganizationModel.objects.all(),
    }
    return render(request, "microdollars/index.html", context)

def about(request):
    return render(request, "microdollars/about.html")

def gamify(request):
    print("form")
    # form = SearchForm(request.POST or None)
    donations = None

    def usernameToUserDonations(username):
        try:
            uid = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        return Donation.objects.filter(user = uid)
    def getAllDonations():
        userList = User.objects.all()
        sum = 0
        leaderboard = []
        for user in userList:
            getUserDonations = usernameToUserDonations(user.username)
            for donation in getUserDonations:
                sum +=donation.amount
            leaderboard.append((user.username, sum))
            sum = 0
        return leaderboard
    print(getAllDonations())
    # if form.is_valid():
    #     # username = form.cleaned_data['user_search']
    #     donations = getAllDonations()
    #     for i in donations:
    #         print(i)
    
    context = {
        # 'form': form,
        'leaderboard': donations,
    }
    
    return render(request, "microdollars/leaderboard.html", context)