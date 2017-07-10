#-*- coding: UTF-8 -*- 
from django.http import HttpResponse
from django.shortcuts import render
import json
import random

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)
    
def ajax_demo(request):
    if request.method == 'POST':
        ret = {'status':False,'message':''}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        print(user,pwd)
        if user == '111' and pwd == '222':
            ret['status'] = True
            return HttpResponse(json.dumps(ret))
        else:
            ret['message'] = '用户名或密码错误'
            return HttpResponse(json.dumps(ret))
    return render(request,'ajax_demo.html')

def UpdateNum(request):
    print "has come here"
    if request.method == 'POST':
        ret = {'returnnum':1}
        print(request.POST.get('mynum'))
        p_num=random.uniform(10, 20)
        ret['returnnum'] = p_num
        print ("random num is  ",p_num)
        return HttpResponse(json.dumps(ret))
    return render(request,'ajax_demo.html')
