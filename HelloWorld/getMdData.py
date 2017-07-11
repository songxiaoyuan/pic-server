# -*- coding:utf8 -*-
import os
import threading
from time import ctime,sleep
from subprocess import Popen,PIPE

import band_and_trigger
import basic_fun

_mdData = None
TradingDay = 0
InstrumentID = 1
LastPrice = 2
Volume = 3
Turnover = 4
OpenInterest =5
UpdateTime = 6
BidPrice1 =7
AskPrice1 =8

def GetMDData(dic):
	# print "start to get the md data and insert to the dic"
	# print "this is init"
	param_dict = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":120
				,"limit_rsi_data":80,"rsi_period":14
				,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
				,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
				,"sd_lastprice":100,"open_interest_edge":0,"spread":100}

	# band_and_trigger_obj = band_and_trigger.BandAndTrigger(param_dict)
	objDict = {}
	path = os.getcwd()+ "\md\mdBasic.exe"
	# path = os.getcwd()+ "\md\\test.exe"
	p = Popen(path,stdout = PIPE,bufsize =10000)
	# print "has start the exe"
	for line in iter(p.stdout.readline,''):
		line = line.split(",")
		# print line
		if len(line) ==9:

			# ret_array = band_and_trigger_obj.get_md_data(line)
			instrumentId = line[InstrumentID].strip()
			if instrumentId not in objDict:
				objDict[instrumentId] = band_and_trigger.BandAndTrigger(param_dict)
			# print instrumentId
			ret_array = objDict[instrumentId].get_md_data(line)
			if instrumentId in dic:
				dic[instrumentId].append(ret_array)
			else:
				dic[instrumentId] = [ret_array]
	p.stdout.close()
	p.terminate()

def getDict():
	return _mdData

import socket,sys
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
try:
	s.bind(('127.0.0.1',8999))
	print "this is called  first"
	if _mdData is None:
		print "this _mdData is none" 
		_mdData = dict()
		brusher = threading.Thread(target=GetMDData,args=(_mdData,))
		brusher.setDaemon(True)
		brusher.start()
		# brusher.join()
		# GetMDData(_mdData)
except:
    print "not bind??"