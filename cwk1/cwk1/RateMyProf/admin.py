from django.contrib import admin
from django.contrib.auth import models as md
from .models import Professor, ModuleInstance, Rating

admin.site.register(Professor)
admin.site.register(ModuleInstance)
admin.site.register(Rating)
