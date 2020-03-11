from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from . import models
import json
import math

# Create your views here.
#For registration#
@csrf_exempt
def register(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if(request.method == 'GET'):
        http_bad_response.content = 'Only POST requests are allowed for this resource\n'
        return http_bad_response

    username = request.POST.get('usrname')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    uniqueUser = True

    if User.objects.filter(username = username).count() > 0:
        uniqueUser = False
    if  User.objects.filter(email = email).count() > 0:
        uniqueUser = False

    if uniqueUser:
        users = User.objects.create_user(username,email,password)
        users.save()
        payload  = {'phrase':"\n\nRegistration successful!!!\n\n"}
        http_response = HttpResponse(json.dumps(payload))
        http_response['Content-Type'] = 'application/json'
        http_response.status_code= 200
        http_response.reason_phrase = 'OK'
        return http_response
    else:
        payload  = {'phrase':"\n\nRegistration Failed!!!\nUsername or email already exists\n\n"}
        http_response = HttpResponse(json.dumps(payload))
        http_response['Content-Type'] = 'application/json'
        http_response.status_code= 401
        http_response.reason_phrase = 'Invalid Credentials'
        return http_response


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if(request.method == 'GET'):
        http_bad_response.content = 'Only POST requests are allowed for this resource\n'
        return http_bad_response

    usrname = request.POST.get('usrname')
    password = request.POST.get('pass')
    user = authenticate(request, username = usrname, password = password)
    if user is not None:
        auth_login(request, user, user.backend)
        token, _ = Token.objects.get_or_create(user=user)
        payload  = {'phrase':"\n\nYou are now logged in!!!\n\n",'token': "Token " + token.key, 'usrname': usrname}
        http_response = HttpResponse(json.dumps(payload))
        http_response['Content-Type'] = 'application/json'
        http_response.status_code= 200
        http_response.reason_phrase = 'OK'
        return http_response
    else:
        payload  = {'phrase':"\n\nError. Login Failed. Invalid credentials or User does not exist. Try again or register first!!!\n\n", 'token': "", 'usrname': ""}
        http_response = HttpResponse(json.dumps(payload))
        http_response['Content-Type'] = 'application/json'
        http_response.status_code= 401
        http_response.reason_phrase = 'Invalid credentials'
        return http_response

#For logout
def logout(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if(request.method != 'GET'):
        http_bad_response.content = 'Only GET requests are allowed for this resource\n'
        return http_bad_response

    token = ""
    payload  = {'phrase':"\n\nYou are now logged out!!!\n\n",'token': token, 'usrname': ""}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code= 200
    http_response.reason_phrase = 'OK'
    return http_response

#For list of modules and teachers and years and semesters
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def list(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if(request.method != 'GET'):
        http_bad_response.content = 'Only GET requests are allowed for this resource\n'
        return http_bad_response

    module_list = models.Module.objects.all().values('module_ID','name','semester','year','teachers')
    the_list = []
    for r in module_list:
        tname = models.Teacher.objects.get(id = r['teachers'])
        string = str(tname.t_ID) + ", " + str(tname.t_name)[0]+ "." + str(tname.t_last_Name)
        item = {'ID':r['module_ID'],'name': r['name'],'sem': r['semester'], 'year': r['year'],'tc': string}
        the_list.append(item)
    payload  = {'phrase':the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code= 200
    http_response.reason_phrase = 'OK'
    return http_response

#For view
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def view(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if(request.method != 'GET'):
        http_bad_response.content = 'Only GET requests are allowed for this resource\n'
        return http_bad_response

    profList = models.Teacher.objects.all()
    the_list = []
    for i in profList:
        rateSum = 0
        avgRate = 0
        trlist = models.Rating.objects.filter(teacher = i.id )
        trcount = models.Rating.objects.filter(teacher = i.id ).count()
        for j in trlist:
            rateSum = rateSum + j.Rating
        if rateSum > 0:
            avgRate = math.trunc((rateSum/trcount) +0.5)
        else:
            avgRate = 0
        name = i.t_name[0] + "." + i.t_last_Name
        item = {'Rating':avgRate,'name': name}
        the_list.append(item)
    payload  = {'phrase':the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code= 200
    http_response.reason_phrase = 'OK'
    return http_response

#For average
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def average(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if(request.method != 'GET'):
        http_bad_response.content = 'Only GET requests are allowed for this resource\n'
        return http_bad_response

    profID = request.POST.get('teach_ID').upper()
    moduleID = request.POST.get('mod_ID').upper()

    teacher = models.Teacher.objects.filter(t_ID = profID).count()
    module = models.Module.objects.filter(module_ID = moduleID ).count()

    if teacher == 0 or module == 0:
        the_list = "\n\nInvalid option\n\n"
        payload  = {'phrase':the_list}
        http_response = HttpResponse(json.dumps(payload))
        http_response['Content-Type'] = 'application/json'
        http_response.status_code= 401
        http_response.reason_phrase = 'Invalid Details'
        return http_response
    else:
        module = models.Module.objects.filter(module_ID = moduleID )[0]
        teacher = models.Teacher.objects.get(t_ID = profID)
        rateSum = 0
        avgRate = 0
        rate = models.Rating.objects.filter(module = module, teacher = teacher.id)
        numModule = models.Module.objects.filter(module_ID = moduleID,teachers = teacher.id).count()
        numRating = models.Rating.objects.filter(module = module, teacher = teacher.id).count()
        if numModule > 0:
            for j in rate:
                rateSum = rateSum + j.Rating
            if rateSum > 0:
                avgRate = math.trunc((rateSum/numRating) + 0.5)
            else:
                avgRate = 0
            name = teacher.t_name[0] + "." + teacher.t_last_Name
            modulename = module.name
            modid = module.module_ID
            item = {'Rating':avgRate,'name': name, 'module_n': modulename, 'modid' : modid}
            payload  = {'phrase':item}
            http_response = HttpResponse(json.dumps(payload))
            http_response['Content-Type'] = 'application/json'
            http_response.status_code= 200
            http_response.reason_phrase = 'OK'
            return http_response

        else:
            the_list = "\n\nTeacher does not take this module.\n\n"
            payload  = {'phrase':the_list}
            http_response = HttpResponse(json.dumps(payload))
            http_response['Content-Type'] = 'application/json'
            http_response.status_code= 401
            http_response.reason_phrase = 'Invalid Details'
            return http_response


#For rate
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def rate(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if(request.method == 'GET'):
        http_bad_response.content = 'Only POST requests are allowed for this resource\n'
        return http_bad_response

    profID = request.POST.get('teach_ID').upper()
    modID = request.POST.get('mod_ID').upper()
    year = request.POST.get('year')
    sem = request.POST.get('semester')
    rate = request.POST.get('rate')

    numProf = models.Teacher.objects.filter(t_ID = profID).count()
    numModule = models.Module.objects.filter(module_ID = modID ).count()
    is_int = isinstance(rate, int)

    if numProf == 0 or numModule == 0 or is_int:
        the_list = "\n\nInvalid option\n\n"
        payload  = {'phrase':the_list}
        http_response = HttpResponse(json.dumps(payload))
        http_response['Content-Type'] = 'application/json'
        http_response.status_code= 401
        http_response.reason_phrase = 'Invalid Details'
        return http_response
    else:
        prof = models.Teacher.objects.get(t_ID = profID)
        module = models.Module.objects.filter(module_ID = modID )[0]
        numModules = models.Module.objects.filter(module_ID = modID,teachers = prof.id, year = int(year), semester = int(sem) ).count()
        if numModules > 0:
            the_list = "\n\nRate successful\n\n"
            payload  = {'phrase':the_list}
            http_response = HttpResponse(json.dumps(payload))
            http_response['Content-Type'] = 'application/json'
            http_response.status_code= 200
            http_response.reason_phrase = 'OK'
            rating = models.Rating.objects.create(module = module,teacher = prof,Rating = rate)
            rating.save()
        else:
            the_list = "\n\nTeacher does not take this module at specified time.\n\n"
            payload  = {'phrase':the_list}
            http_response = HttpResponse(json.dumps(payload))
            http_response['Content-Type'] = 'application/json'
            http_response.status_code= 401
            http_response.reason_phrase = 'Invalid Details'
            return http_response
        return http_response
