from django.db import models

class OrganizationModel(models.Model):
    organization_name = models.CharField(max_length=100)
    about_me = models.TextField(max_length = 1000, default='INFO ON THIS ORGANIZATION')

    def __str__(self):
        return self.organization_name


# {% comment %}
# /***************************************************************************************
# *  REFERENCES
# *  Title: How to Implement Dependent/Chained Dropdown List with Django
# *  Author: Vitor Freitas
# *  Date: 1/29/18
# *  Code version: N/A
# *  URL: https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
# *  Software License: Part of a tutorial
# *
# ***************************************************************************************/
# {% endcomment %}
class Donation(models.Model):
    # user = models.ForeignKey(models.User, on_delete=models.SET_NULL, null=TRUE)
    donateto = models.ForeignKey(OrganizationModel, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField()
    comment = models.CharField(max_length=350)

    def convertToTuple(self, info):
        obj = info.objects.all()
