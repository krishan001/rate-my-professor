import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.http import Http404
from django.shortcuts import render

# Create your views here.

authenticated = False
g_user = ""

@csrf_exempt
def register(request):
    username = request.GET.get("username")
    email = request.GET.get("email")
    password = request.GET.get("password")
    user = User.objects.create_user(username,email,password)
    user.save()


@csrf_exempt
def login_validate(request):
    global authenticated
    global g_user
    username = request.GET.get('username')
    password = request.GET.get('password')
    #authenticate the user
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        #login the user
        login(request, user)
        g_user = request.user
        payload = "Successfully logged in"
        http_response = HttpResponse(payload)
        http_response['Content-Type'] = 'text/plain'
        http_response_code = 200
        http_response.reason_phrase = 'OK'
        authenticated = (request.user.is_authenticated)
        return http_response

    else:
        payload = "Wrong log in information"
        http_response = HttpResponse(payload, status=403)
        http_response['Content-Type'] = 'text/plain'
        http_response_code = 403
        http_response.reason_phrase = ""
        return http_response

@csrf_exempt
def logout_validate(request):
    global authenticated
    if authenticated:
        logout(request)
        payload = "Successfully logged out"
        http_response = HttpResponse(payload)
        http_response['Content-Type'] = 'text/plain'
        http_response_code = 200
        http_response.reason_phrase = "OK"
        authenticated=False
        g_user=None
        return http_response
    else:
        payload = "Not logged in"
        http_response = HttpResponse(payload, status=403)
        http_response['Content-Type'] = 'text/plain'
        http_response_code = 403
        http_response.reason_phrase = ""
        return http_response


@csrf_exempt
def get_list(request):
    pass

@csrf_exempt
def get_view(request):
    pass

@csrf_exempt
def get_average(request):
    pass

@csrf_exempt
def post_rating(request):
    pass
