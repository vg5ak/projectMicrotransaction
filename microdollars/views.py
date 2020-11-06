from django.shortcuts import render
from django.views.generic import CreateView
from .models import Donation, OrganizationModel, Search
from django.contrib.auth.models import User
from microdollars.forms import DonationForm, SearchForm, Search
from django.core.exceptions import ObjectDoesNotExist
from collections import Counter 
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
    ystuff = None
    xstuff = None
    def usernameToUserDonations(username):
        try:
            uid = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        return Donation.objects.filter(user = uid)


    def GraphY(username):
        orginal_list = [] 
        Org_dict = { 1 : "Boys and Girls Association",  2: "Alcoholics Anonymous", 3: "World Wildlife Fund" , 
        4 : "The Salvation Army" ,  5: "Doctors Without Borders USA", 6: "American National Red Cross"}
        try:
            ##Get's all donations objects that have the been donated by the USER
            user_donations = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

        Pie_data = Donation.objects.filter(user = user_donations).values_list("donateto")
        Pie_data = list(Pie_data)
       
        orginal_list.append(Pie_data)
        maybe = [x[0] for x in Pie_data]
        please = [Org_dict[i] for i in maybe]

        return list(Counter(please).keys())
    def GraphX(username):
        orginal_list = [] 
 

        Org_dict = { 1 : "Boys and Girls Association",  2: "Alcoholics Anonymous", 3: "World Wildlife Fund" , 
        4 : "The Salvation Army" ,  5: "Doctors Without Borders USA", 6: "American National Red Cross"}
        try:
            ##Get's all donations objects that have the been donated by the USER
            user_donations = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

        Pie_data = Donation.objects.filter(user = user_donations).values_list("donateto")
        Pie_data = list(Pie_data)
       
        orginal_list.append(Pie_data)
        maybe = [x[0] for x in Pie_data]
        please = [Org_dict[i] for i in maybe]
        #Counter(please).keys() = ydata
        
        return list(Counter(please).values())

    if form.is_valid():
        username = form.cleaned_data['user_search']
        print(username)
        donations = usernameToUserDonations(username)
        
        ystuff = GraphY(username)
        print(ystuff)
        xstuff = GraphX(username)
        print(xstuff)
        #print(test)
    ###Get's all the donations that they donated to
    
    # def GetOrganizations(username):
    #     try:
    #         orgs = User.objects.get(username = username)
    #     except ObjectDoesNotExist:
    #         return None
    #     return OrganizationModel.objects.get(user = orgs)

    # ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
  
  
    context = {
        'form': form,
        'donation_list_search': donations,
        'data': xstuff,
        'labels': ystuff,

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

