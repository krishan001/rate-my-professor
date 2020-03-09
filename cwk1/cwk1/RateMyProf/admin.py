from django.contrib import admin
from django.contrib.auth import models as md
from .models import Teacher, Module, Rating

admin.site.register(Teacher)
admin.site.register(Module)
admin.site.register(Rating)
