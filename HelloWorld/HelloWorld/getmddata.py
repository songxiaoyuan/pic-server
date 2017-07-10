import os
from subprocess import Popen,PIPE
# md = ":\\md\\mdBasic.exe"
# # p = Popen(md,stdout = PIPE,bufsize =10000)
# # for line in iter(p.stdout.readline,''):
# # 	line = line.split(",")
# # 	print type(line)
# # 	print line
# # os.system(md)
# path =  os.getcwd()
# path = path + "\md\mdBasic.exe"
# # print path
# os.system(path)
def GetMDData(dic):
	# print "start to get the md data and insert to the dic"
	path = os.getcwd()+ "\md\mdBasic.exe"
	p = Popen(path,stdout = PIPE,bufsize =10000)
	for line in iter(p.stdout.readline,''):
		line = line.split(",")
		if len(line) ==9:
			instrumentId = line[1].strip()
			if instrumentId in dic:
				dic[instrumentId].append(line)
			else:
				dic[instrumentId] = [line]


if __name__ == '__main__':
	dic = dict()
	GetMDData(dic)
	print dic