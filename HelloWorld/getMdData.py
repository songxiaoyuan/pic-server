# -*- coding:utf8 -*-
import os
import cx_Oracle
import threading
import time
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

SQL_LASTPRICE = 4
SQL_VOLUME = 11
SQL_OPENINTEREST = 13
SQL_TURNONER = 12
SQL_BIDPRICE1 = 22
SQL_ASKPRICE1 =24
SQL_TIME = 20
SQL_DATA = 0
SQL_INSTRUMENT = 1


# 这个是铅的
param_dict_pb = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":50
			,"limit_rsi_data":75,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":20,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":310}
# 这个是螺纹钢的
param_dict_rb = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":320}

# 这个是锌的
param_dic_zn = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":346}
# 这个是橡胶的
param_dic_ru = {"limit_max_profit":250,"limit_max_loss":100,"rsi_bar_period":100
			,"limit_rsi_data":70,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":330}

nameDict = {
	"rb1710":{"param":param_dict_rb},
	"ru1801":{"param":param_dic_ru},
	"zn1709":{"param":param_dic_zn},
	"pb1709":{"param":param_dict_pb}
}

def getSortedData(data):
	ret = []
	night = []
	zero = []
	day = []
	nightBegin = 21*3600
	nightEnd = 23*3600+59*60+60
	zeroBegin = 0
	zeroEnd = 9*3600 - 100
	dayBegin = 9*3600
	dayEnd = 15*3600

	for line in data:
		# print line
		timeLine = line[20].split(":")
		# print timeLine
		nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])

		if nowTime >= zeroBegin and nowTime <zeroEnd:
			zero.append(line)
		elif nowTime >= dayBegin and nowTime <= dayEnd:
			day.append(line)
		elif nowTime >=nightBegin and nowTime <=nightEnd:
			night.append(line)
		# if int(line[22]) ==0 or int(line[4]) ==3629:
		# 	continue
	# for line in night:
	# 	ret.append(line)
	# for line in zero:
	# 	ret.append(line)
	for line in day:
		ret.append(line)

	return ret

def getInstrumentsIds():
	for line in open("config.txt"):
		line = line.strip().split(" ")
		# print line
		if len(line) ==2 and line[0] =="INSTRUMENT":
			return line[1].split(',')

def getSqlData():
	ret = []
	print "start to get the sql data"
	date = time.strftime('%Y%m%d',time.localtime(time.time()))
	instrumentsids_array = getInstrumentsIds()
	print instrumentsids_array

	conn = cx_Oracle.connect('hq','hq','114.251.16.210:9921/quota')    
	cursor = conn.cursor () 
	for instrumentId in instrumentsids_array:
		mysql="select *from hyqh.quotatick where TRADINGDAY = '%s' AND instr(INSTRUMENTID,'%s')>0" % (date,instrumentId)

		print mysql
		cursor.execute (mysql)  

		icresult = cursor.fetchall()
		# get the data and sort it.
		sortedlist = sorted(icresult, key = lambda x: (x[20], int(x[21])))
		# remove the 00:00 and 21:00 data,we dont need it
		cleandata = getSortedData(sortedlist)
		for line  in cleandata:
			tmp = [line[SQL_DATA],line[SQL_INSTRUMENT],line[SQL_LASTPRICE],
			line[SQL_VOLUME],line[SQL_TURNONER],line[SQL_OPENINTEREST],line[SQL_TIME],
			line[SQL_BIDPRICE1],line[SQL_ASKPRICE1],]
			ret.append(tmp)

	cursor.close ()  
	conn.close () 
	return ret

def GetMDData(dic):
	# print "start to get the md data and insert to the dic"
	print "get the before sql data"
	sqlData = getSqlData()
	path = os.getcwd()+ "\md\mdBasic.exe"
	# path = os.getcwd()+ "\md\\test.exe"
	p = Popen(path,stdout = PIPE,bufsize =10000)
	print "the mdBasic.exe has been  started"
	print "starting to start the mdBasic.exe"
	param_dict = {"limit_max_profit":25,"limit_max_loss":6,"rsi_bar_period":100
					,"limit_rsi_data":80,"rsi_period":10,"band_period_begin":7200,"diff_period":1
					,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
					,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
					,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"limit_sd":4,"limit_sd_open_edge":1
					,"limit_sd_close_edge":3}

	# band_and_trigger_obj = band_and_trigger.BandAndTrigger(param_dict)
	objDict = {}
	for line  in sqlData:
		instrumentId = line[InstrumentID].strip()
		if "SP" in instrumentId:
			continue
		if instrumentId not in objDict:
			objDict[instrumentId] = band_and_trigger.BandAndTrigger(nameDict[instrumentId]["param"])
		# print instrumentId
		ret_array = objDict[instrumentId].get_md_data(line)
		if len(ret_array) ==0:
			continue
		if instrumentId in dic:
			dic[instrumentId].append(ret_array)
		else:
			dic[instrumentId] = [ret_array]

	print "the sql data has been caculated!"
	for line in iter(p.stdout.readline,''):
		line = line.split(",")
		# print line
		if len(line) ==9:

			# ret_array = band_and_trigger_obj.get_md_data(line)
			instrumentId = line[InstrumentID].strip()
			if instrumentId not in objDict:
				objDict[instrumentId] = band_and_trigger.BandAndTrigger(nameDict[instrumentId]["param"])
			# print instrumentId
			ret_array = objDict[instrumentId].get_md_data(line)
			if len(ret_array) ==0:
				continue
			if instrumentId in dic:
				dic[instrumentId].append(ret_array)
			else:
				dic[instrumentId] = [ret_array]
	p.stdout.close()
	p.terminate()

def getDict():
	return _mdData

print "this is the init function. start the mdBasic.exe"
import socket,sys
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
try:
	s.bind(('127.0.0.1',9001))
	print "this is called  first"
	if _mdData is None:
		print "this _mdData is none and start to init it" 
		_mdData = dict()
		brusher = threading.Thread(target=GetMDData,args=(_mdData,))
		brusher.setDaemon(True)
		brusher.start()
	else:
		print "the _mdData is not none"
except:
    print "the sortket has been bind"
