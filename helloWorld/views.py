from django.shortcuts import render

import datetime
from django.http import HttpResponse

from . import models

# Create your views here.
def helloworld(request):
    return render(request, 'helloworld.html')


def hello(request):
    params = {}
    params['hello'] = 'Hello World!'
    params['list_eg'] = ['aa', 'bb', 'cc']
    params['empty_list'] = []
    params['dict_eg'] = {'my_key': 'my_value', 'a_key': 'a_value'}
    params['today'] = datetime.datetime.now()
    params['my_name'] = 0 # it's bool is false, thus will use default in page
    params['a_file_size'] = 1024
    params['safe_tag'] = "<a href='https://www.google.com/'>click</a>"
    params['score'] = 98
    
    return render(request, 'hellopage.html', params)

# database operation
def testdb(request):
    
    # add a row
    test1 = models.HelloTestModels(name='sihan')
    test1.save()
    return HttpResponse("<p>successfully add data！</p>")
    
    # # init
    # response = ""
    # response1 = "" 
    # # all() equal to SELECT * FROM
    # list = models.HelloTestModels.objects.all()      
    # # filter() equal to WHERE
    # response2 = models.HelloTestModels.objects.filter(id=1)   
    # # [0:2] equal to OFFSET 0 LIMIT 2;
    # models.HelloTestModels.objects.order_by('name')[0:2]  
    # # order by
    # models.HelloTestModels.objects.order_by("id")
    # # combination of methods
    # models.HelloTestModels.objects.filter(name="sihan").order_by("id")
    # # output all
    # for var in list:
    #     response1 += var.name + " "
    # response = response1
    # return HttpResponse("<p>" + response + "</p>")
    
    # # equal to update UPDATE
    # test1 = models.HelloTestModels.objects.get(id=1)
    # test1.name = 'Google'
    # test1.save()
    
    # # another way to UPDATE
    # #models.HelloTestModels.objects.filter(id=1).update(name='Google')
    
    # # UPDATE ALL
    # # models.HelloTestModels.objects.all().update(name='Google')
    
    # return HttpResponse("<p>update success</p>")
    
    # # DELETE
    # test1 = models.HelloTestModels.objects.get(id=1)
    # test1.delete()
    
    # # another way to DELETE
    # # models.HelloTestModels.objects.filter(id=1).delete()
    
    # # DELETE ALL
    # # models.HelloTestModels.objects.all().delete()
    
    # return HttpResponse("<p>delete success</p>")