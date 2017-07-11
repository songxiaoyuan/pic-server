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

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []
		self._pre_ema_val = 0
		self._now_middle_value =0
		self._now_sd_val = 0

		self._max_profit = 0
		self._limit_max_draw_down = param_dic["limit_max_draw_down"]
		self._limit_max_profit = param_dic["limit_max_profit"]
		self._limit_max_loss = param_dic["limit_max_loss"]

		self._multiple = param_dic["multiple"]

		self._rsi_array = []
		self._rsi_period = param_dic["rsi_period"]
		self._pre_rsi_lastprice =0 
		self._now_bar_rsi_tick = 0
		self._rsi_bar_period = param_dic["rsi_bar_period"]
		self._limit_rsi_data = param_dic["limit_rsi_data"]


		# self._limit_twice_sd = 2

		self._moving_theo = "EMA"
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1

		# band param
		self._param_open_edge = param_dic["band_open_edge"]
		self._param_loss_edge = param_dic["band_loss_edge"]
		self._param_close_edge =param_dic["band_profit_edge"]
		self._param_period = param_dic["band_period"]
		
		# if the sd is too small like is smaller than _param_limit_sd_value,
		# the open edge and close edge will bigger 
		# self._param_limit_sd_value = limit_sd_val
		# self._param_limit_bigger = 0

		# trigger param
		self._param_volume_open_edge = param_dic["volume_open_edge"]
		self._param_open_interest_edge = param_dic["open_interest_edge"]
		self._param_spread = param_dic["spread"]

		self._open_lastprice = 0
		self._profit = 0
		self._ris_data = 0

		self._sd_lastprice = param_dic["sd_lastprice"]

		self._file = param_dic["file"]


	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		md_array[LastPrice] = float(md_array[LastPrice])
		md_array[Volume] = float(md_array[Volume])
		md_array[OpenInterest] = float(md_array[OpenInterest])
		md_array[Turnover] = float(md_array[Turnover])
		md_array[BidPrice1] = float(md_array[BidPrice1])
		md_array[AskPrice1] = float(md_array[AskPrice1])


		self._pre_md_price = self._now_md_price
		self._now_md_price = md_array

		lastprice = self._now_md_price[LastPrice]
		self._lastprice_array.append(lastprice)
		# print lastprice

		if len(self._pre_md_price) ==0:
			self._rsi_array.append(0)
			self._pre_rsi_lastprice = lastprice
			self._ris_data = -1
			# self._rsi_array.append(0)
		else:
			# self._rsi_array.append(lastprice - self._pre_md_price[LASTPRICE])
			if self._now_bar_rsi_tick >= self._rsi_bar_period:
				# 表示已经到了一个bar的周期。
				tmpdiff = lastprice - self._pre_rsi_lastprice		
				self._pre_rsi_lastprice = lastprice
				self._now_bar_rsi_tick = 1
				self._ris_data =bf.get_rsi_data2(tmpdiff,self._rsi_array,self._rsi_period)
				self._rsi_array.append(tmpdiff)
			else:
				self._now_bar_rsi_tick +=1
				tmpdiff = lastprice - self._pre_rsi_lastprice
				self._ris_data =bf.get_rsi_data2(tmpdiff,self._rsi_array,self._rsi_period)
				# self._ris_data = 0

		if len(self._lastprice_array)-1 < self._param_period:
			# this is we dont start the period.
			ema_period = len(self._lastprice_array)
			pre_ema_val = bf.get_ema_data(lastprice,self._pre_ema_val,ema_period)
			self._pre_ema_val = pre_ema_val
			self._now_sd_val =bf.get_sd_data(self._now_md_price[UpdateTime], self._lastprice_array,ema_period)
			# save the pre_ema_val and return
			# return True
			ret = [self._now_md_price[LastPrice],self._pre_ema_val,self._now_sd_val,self._now_md_price[UpdateTime]]
			return ret

		# start the judge
		if self._moving_theo =="EMA":
			self._now_middle_value = bf.get_ema_data(lastprice,self._pre_ema_val,self._param_period)
			self._pre_ema_val = self._now_middle_value
		else:
			self._now_middle_value = bf.get_ma_data(self._lastprice_array,self._param_period)
		
		self._now_sd_val =bf.get_sd_data(self._now_md_price[UpdateTime],self._lastprice_array,self._param_period)	
		
		# diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]
		# diff_openinterest = self._now_md_price[OPENINTEREST] - self._pre_md_price[OPENINTEREST]

		# # self.f.write(str(self._now_md_price[TIME])+","+str(lastprice)+","+str(self._now_middle_value)+","+str(self._now_sd_val)+","+str(self._ris_data)+"\n")
		# diff_turnover = self._now_md_price[TURNONER] - self._pre_md_price[TURNONER]

		# avg_price = float(diff_turnover)/diff_volume/self._multiple
		# spread = 100*(self._pre_md_price[ASKPRICE1] - avg_price)/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])


		ret = [self._now_md_price[LastPrice],self._now_middle_value,self._now_sd_val,self._now_md_price[UpdateTime]]
		return ret




if __name__=='__main__': 
	print "this is the band and trigger size"