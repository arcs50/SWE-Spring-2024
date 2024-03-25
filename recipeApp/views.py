from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the recipeApp index.")

def subscriber_home(request):
    params = {}
    return render(request, 'subhomepage.html', params)