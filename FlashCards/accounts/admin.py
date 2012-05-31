from django.contrib import admin
from  models import *

class Admin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, Admin)