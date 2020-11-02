from django.test import TestCase

# Create your tests here.
from .models import OrganizationModel, Donation
from .forms import DonationForm
from http import HTTPStatus
from django.contrib.auth.models import User


class OrganizationTest(TestCase):
    # Donation.objects.create()
    # assertEquals("RequiredOutput", This DonationModel.str())
    def create_org(self):
        return OrganizationModel.objects.create()

    def test_about_me(self):
        item = self.create_org()
        self.assertEquals("INFO ON THIS ORGANIZATION", item.about_me)

    def test_organization_name(self):
        item = self.create_org()
        self.assertEquals(item.organization_name, "")

    def test_false_name(self):
        item = self.create_org()
        self.assertNotEqual(item.organization_name, "Anything")

    def test_false_about_me(self):
        item = self.create_org()
        self.assertNotEqual(item.about_me, "INFO ON THIS ORGANIZATIO")


class DonationFormTests(TestCase):
    # check whether form properly pulls orgs from the DB and displays in the form
    def test_donateto_field_contains_all_orgnizations(self):
        OrganizationModel.objects.create(
            organization_name="Org 1", about_me="I'm Org 1!")
        form = DonationForm()
        OrganizationModel.objects.create(
            organization_name="Org 2", about_me="I'm Org 2!")
        self.assertQuerysetEqual(
            form.fields['donateto'].queryset, OrganizationModel.objects.all(), transform=lambda x: x, ordered=False)

    def test_success_donation_form(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        formData = {
            'donateto': org,
            'amount': 55,
            'comment': "55 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertTrue(form.is_valid())

    def test_improperOrg_donation_from(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        uncontainedOrg = OrganizationModel(
            organization_name="Org 2", about_me="I'm Org 2!")

        formData = {
            'donateto': uncontainedOrg,
            'amount': 55,
            'comment': "55 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertFalse(form.is_valid())

    def test_improperAmountString_donation_from(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        formData = {
            'donateto': org,
            'amount': "not a number",
            'comment': "55 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertFalse(form.is_valid())

    def test_improperAmountNegative_donation_from(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        formData = {
            'donateto': org,
            'amount': -1,
            'comment': "-1 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertFalse(form.is_valid())

    def test_improperAmountZero_donation_from(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        formData = {
            'donateto': org,
            'amount': 0,
            'comment': "-1 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertFalse(form.is_valid())

# Integration test: submit with the form & view


class DonationFormAndViewTest(TestCase):
    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, '<label for="id_donateto">Donate to:</label>', html=True)

    def test_submitForm(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        user.save()

        self.assertEqual(Donation.objects.count(), 0)
        response = self.client.post(
            "/", data={"user": user.id, "donateto": org.id, "amount": 50, "comment": "Here's 50 dollars"}
        )
        self.assertEqual(Donation.objects.count(), 1)
