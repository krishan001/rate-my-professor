
from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
path('api/register/', views.register, name='register'),
path('api/login/', views.login, name='login'),
path('api/logout/', views.logout, name='logout'),
path('api/list/', views.list, name='list'),
path('api/view/', views.view, name='view'),
path('api/average/', views.average, name='average'),
path('api/rate/', views.rate, name='rate'),
]
