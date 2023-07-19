from django.contrib import admin
from Shop.models import *

# class AdminInterface(admin.ModelAdmin):
#     Info=['name']
admin.site.register(Category)
admin.site.register(Product)

# Register your models here.
