from django.contrib import admin
from .models import Module, Prof, Student, Rating, ModuleInstance
# Register your models here.

admin.site.register(Module)
admin.site.register(Prof)
admin.site.register(ModuleInstance)
admin.site.register(Student)
admin.site.register(Rating)
