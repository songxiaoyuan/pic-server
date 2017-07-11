import os
import threading
from time import ctime,sleep
from subprocess import Popen,PIPE

def GetMDData(dic):
	# print "start to get the md data and insert to the dic"
	# path = os.getcwd()+ "\md\mdBasic.exe"
	path = os.getcwd()+ "\md\\test.exe"
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

def printDic(dic):
	while True:
		sleep(5)
		print dic

def main():
	dic = dict()
	threads = []
	t1 = threading.Thread(target=GetMDData,args=(dic,))
	threads.append(t1)
	t2 = threading.Thread(target=printDic,args=(dic,))
	threads.append(t2)
	print dic
	for t in threads:
	    t.setDaemon(True)
	    t.start()
	print "out"
	t1.join()
	t2.join()

if __name__ == '__main__':
	main()