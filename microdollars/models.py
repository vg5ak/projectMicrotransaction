from django.db import models

# Create your models here.
# "This is a new comment"
# class BaseModel(model.BaseModel):
#     name = models.TextField()
#     class Meta:
#         abstract = True


class OrganizationModel(models.Model):
    organization_name = models.CharField(max_length=100)
    about_me = models.TextField(max_length = 1000, default='INFO ON THIS ORGANIZATION')
    # total_donations = ''
    # your_donation = ''
    def __str__(self):
        return self.organization_name



class Donation(models.Model):
    ORGANIZATION_CHOICES = [
        ('red cross', 'Red Cross'),
        ('non-profit #1', 'Non-profit #1'),
        ('non-profit #2', 'Non-profit #2'),
    ]

    donateto = models.ForeignKey(OrganizationModel, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField()
    comment = models.CharField(max_length=350)

    def convertToTuple(self, info):
        obj = info.objects.all()
