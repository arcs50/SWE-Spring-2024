from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the recipeApp index.")

def discover(request):
    params = {}   
    if request.user.is_authenticated:
        params['is_authenticated'] = True
        params['avator_dir'] = 'images/sad_cat.jpg'
    
    return render(request, 'discover.html', params)

def subscriber_home(request):
    params = {}
    return render(request, 'subhomepage.html', params)