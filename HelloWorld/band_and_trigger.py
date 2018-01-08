# -*- coding:utf8 -*-
import basic_fun as bf

TradingDay = 0
InstrumentID = 1
LastPrice = 2
Volume = 3
Turnover = 4
OpenInterest =5
UpdateTime = 6
BidPrice1 =7
AskPrice1 =8
LONG =1
SHORT =0

nameDict = {
	"rb":1,
	"ru":5,
	"zn":5,
	"cu":10,
	"hc":1,
	"ni":10,
	"al":5,
	"au":0.05,
	"ag":1,
	"pp":1,
	"v":5,
	"bu":2,
	"pb":5
}


class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,instrument_id):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._total_max_lastprice = 0
		self._total_min_lastprice = 0

		self._day_max_lastprice = 0
		self._day_min_lastprice = 0

		self._tick = nameDict[instrument_id[0:2]]


	def is_day(self,time):
		nightBegin = 21*3600
		nightEnd = 23*3600+59*60+60
		zeroBegin = 0
		zeroEnd = 9*3600 - 100
		dayBegin = 9*3600
		dayEnd = 15*3600

		timeLine = time.split(":")
			# print timeLine
		try:
			nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])
		except Exception as e:
			nowTime = 0

		if nowTime >= zeroBegin and nowTime <zeroEnd:
			return False
		elif nowTime >= dayBegin and nowTime <= dayEnd:
			return True
		elif nowTime >=nightBegin and nowTime <=nightEnd:
			return False

	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		lastprice = float(md_array[LastPrice])

		is_day_now = self.is_day(md_array[UpdateTime])
		if is_day_now == True:
			if self._total_min_lastprice ==0 or self._total_min_lastprice > lastprice:
				self._total_min_lastprice = lastprice
			if self._total_max_lastprice ==0  or self._total_max_lastprice < lastprice:
				self._total_max_lastprice = lastprice
			if self._day_min_lastprice ==0 or self._day_min_lastprice > lastprice:
				self._day_min_lastprice = lastprice
			if self._day_max_lastprice ==0  or self._day_max_lastprice < lastprice:
				self._day_max_lastprice = lastprice
		else:
			if self._total_min_lastprice ==0 or self._total_min_lastprice > lastprice:
				self._total_min_lastprice = lastprice
			if self._total_max_lastprice ==0  or self._total_max_lastprice < lastprice:
				self._total_max_lastprice = lastprice
		
		total_range = (self._total_max_lastprice - self._total_min_lastprice)/self._tick
		day_range = (self._day_max_lastprice - self._day_min_lastprice)/self._tick
		ret = [total_range,day_range]
		return ret




if __name__=='__main__': 
	print "this is the band and trigger size"