from django.contrib import admin
from .models import Profile

# Registers Profile to be managable by  admin
class profileAdmin(admin.ModelAdmin):
    list_display=['user', 'sex','date_of_birth', 'occupation']
admin.site.register(Profile, profileAdmin)
