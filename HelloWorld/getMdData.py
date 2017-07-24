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


def cleanMdData(data):
	ret = []
	amBegin = 9*3600
	amEnd = 11*3600+30*60
	pmBegin = 13*3600+30*60
	pmEnd = 15*3600
	amRestBegin = 10*3600+15*60
	amRestEnd = 10*3600+30*60

	for line in data:
		# print line
		timeLine = line[20].split(":")
		# print timeLine
		# tick = line[21]
		nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])
		# print nowTime
		# print time
		# import pdb
		# pdb.set_trace()
		if nowTime<amBegin:
			continue
		if nowTime>pmEnd:
			break
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
		cleandata = cleanMdData(sortedlist)
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
	param_dict = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":100
				,"limit_rsi_data":80,"rsi_period":10
				,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
				,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
				,"sd_lastprice":100,"open_interest_edge":0,"spread":100}

	# band_and_trigger_obj = band_and_trigger.BandAndTrigger(param_dict)
	objDict = {}
	for line  in sqlData:
		instrumentId = line[InstrumentID].strip()
		if "SP" in instrumentId:
			continue
		if instrumentId not in objDict:
			objDict[instrumentId] = band_and_trigger.BandAndTrigger(param_dict)
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
				objDict[instrumentId] = band_and_trigger.BandAndTrigger(param_dict)
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
	s.bind(('127.0.0.1',9000))
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
