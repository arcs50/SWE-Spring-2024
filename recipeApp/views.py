from django.http import HttpResponse
from django.shortcuts import render
import datetime

def welcome(request):
    return render(request, 'welcome.html')
 