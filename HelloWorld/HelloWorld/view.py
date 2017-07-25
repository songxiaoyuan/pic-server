#-*- coding: UTF-8 -*- 
from django.http import HttpResponse
from django.shortcuts import render
import json
import random
# import getMdData
import getMACDData

# print "this is in view"
# print id(test._g)

def index(request):
    context          = {}
    if getMdData._mdData ==None:
        context["data"]={"has instrumentid":[]}
    else:
        context["data"] = getMdData._mdData
    # print context
    return render(request, 'index.html', context)

def index_macd(request):
    print "start to get the macd"
    context          = {}
    if getMACDData._macdData ==None:
        context["data"]={"has instrumentid":[]}
    else:
        context["data"] = getMACDData._macdData
    # print context
    return render(request, 'index_macd.html', context)

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
    # print "has come here"
    if request.method == 'POST':
        ret = {'returnnum':1}
        # print(request.POST.get('mynum'))
        p_num=random.uniform(10, 20)
        ret['returnnum'] = p_num
        # print ("random num is  ",p_num)
        return HttpResponse(json.dumps(ret))
    return render(request,'ajax_demo.html')

def UpdateMdData(request):
    # base the url to get the instrumentid
    if request.method == 'GET':
        instrumentid = request.GET.get('instrumentid')
        # print instrumentid
        ret = {}
        ret["instrumentid"] = instrumentid
        return render(request,'show_band.html',ret)
    if request.method == 'POST':
        # this is the ajax ,return the dict data
        ret = {'data':""}
        # print "this is post"
        instrument = request.POST.get('instrumentid').decode("utf-8")
        print instrument
        if getMdData._mdData ==None:
            print "the md data is  none, please find the reason"
        elif instrument in getMdData._mdData:
            ret["data"] = getMdData._mdData[instrument]
        return HttpResponse(json.dumps(ret))
    return render(request,'show_band.html')

def UpdateMACDData(request):
    # base the url to get the instrumentid
    if request.method == 'GET':
        instrumentid = request.GET.get('instrumentid')
        # print instrumentid
        ret = {}
        ret["instrumentid"] = instrumentid
        return render(request,'show_macd.html',ret)
    if request.method == 'POST':
        # this is the ajax ,return the dict data
        ret = {'data':""}
        # print "this is post"
        instrument = request.POST.get('instrumentid').decode("utf-8")
        print instrument
        if getMACDData._macdData ==None:
            print "the md data is  none, please find the reason"
        elif instrument in getMACDData._macdData:
            ret["data"] = getMACDData._macdData[instrument]
        return HttpResponse(json.dumps(ret))
    return render(request,'show_macd.html')
