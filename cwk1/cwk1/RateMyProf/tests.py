from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.http import HttpRequest, HttpResponseBadRequest
import json




# Create your tests here.
request = HttpRequest()
def lists():
    r = request.get('https://127.0.0.1:8000/api/list')
    lists = []
    for i in r['list']:
        lists.append(i)
    print(lists)

lists()
