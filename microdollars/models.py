from django.db import models

# Create your models here.
# "This is a new comment"
# class BaseModel(model.BaseModel):
#     name = models.TextField()
#     class Meta:
#         abstract = True

ORGANIZATION_CHOICES= (
    ('red cross', 'Red Cross'),
    ('non-profit #1', 'Non-profit #1'),
    ('non-profit #2', 'Non-profit #2'),
)

class Donation(models.Model):
    donateto = models.CharField(max_length=30, choices=ORGANIZATION_CHOICES, default='Red Cross')
    amount = models.PositiveIntegerField()
    comment = models.CharField(max_length=350)
