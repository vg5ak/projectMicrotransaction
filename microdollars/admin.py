from django.contrib import admin

# Register your models here.
#test
from .models import OrganizationModel as O
#import Organization Model into admin
admin.site.register(O)
