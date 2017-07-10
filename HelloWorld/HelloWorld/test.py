_g = None
import os
import threading
from time import ctime,sleep
from subprocess import Popen,PIPE


def GetMDData(dic):
	# print "start to get the md data and insert to the dic"
	print "this is init"
	path = os.getcwd()+ "\md\mdBasic.exe"
	p = Popen(path,stdout = PIPE,bufsize =10000)
	for line in iter(p.stdout.readline,''):
		line = line.split(",")
		if len(line) ==9:
			instrumentId = line[1].strip()
			# print instrumentId
			if instrumentId in dic:
				dic[instrumentId].append(line)
			else:
				dic[instrumentId] = [line]
	p.stdout.close()
	p.terminate()

def getDict():
	return _g

import socket,sys
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
try:
	s.bind(('127.0.0.1',10086))
	if _g is None:
		print "this is called  first" 
		_g = dict()
	brusher = threading.Thread(target=GetMDData,args=(_g,))
	brusher.setDaemon(True)
	brusher.start()
	brusher.join()
except:
    pass