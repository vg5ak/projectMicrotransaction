from django.test import TestCase

# Create your tests here.
from .models import  OrganizationModel, Donation

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

    def test_false_name(self):
        item = self.create_org()
        self.assertNotEqual(item.organization_name, "Anything")
    def test_false_about_me(self):
        item = self.create_org()
        self.assertNotEqual(item.about_me, "INFO ON THIS ORGANIZATIO")

#class DonationTest(TestCase):
    #def create_donate(self):
        #return Donation.objects.create()
    #def test_comment(self):
        #item = self.create_donate()
        #self.assertContains(item.comment, "")
    
