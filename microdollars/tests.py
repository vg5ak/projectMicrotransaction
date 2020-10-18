from django.test import TestCase

# Create your tests here.
from .models import  OrganizationModel, Donation

class OrganizationModel(TestCase):
    def information_is_readable(self):
        self.assertTrue(OrganizationModel.aboutme)
    
class Donation(TestCase):
    def not_negative(self):
        self.assertFalse(Donation.amount>= 0)