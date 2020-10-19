from _typeshed import NoneType
from django.db.models.fields import NullBooleanField
from microdollars.forms import DonationForm
from microdollars.models import Donation, OrganizationModel
from django.test import TestCase
from django.test import TestCase
# Create your tests here.


class OrganizationTest(TestCase):
    #Donation.objects.create() 
    #assertEquals("RequiredOutput", This DonationModel.str())
    def create_org(self):
        return OrganizationModel.objects.create()

    def test_about_me(self):
        item = self.create_org()
        self.assertEquals("INFO ON THIS ORGANIZATION", item.about_me )
    
    def test_organization_name(self):
        item = self.create_org()
        self.assertEquals(item.organization_name, "")

    def test_false_tests(self):
        item = self.create_org()
        self.assertNotEqual(item.about_me, "Anything else")
        self.assertNotEqual(item.organization_name, "Red Cross")


class DonationTest(TestCase):
    def create_donation(self):
        return Donation.objects.create()
    
    def test_comment(self):
        donate = self.create_donation()
        self.assertEquals(donate.comment, "")
