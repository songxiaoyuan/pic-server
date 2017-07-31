# -*- coding:utf8 -*-
import os
import cx_Oracle
import threading
import time
from time import ctime,sleep
from subprocess import Popen,PIPE


import band_and_trigger
import basic_fun

_macdData = None
TradingDay = 0
InstrumentID = 1
LastPrice = 2
Volume = 3
Turnover = 4
OpenInterest =5
UpdateTime = 6
BidPrice1 =7
AskPrice1 =8


_macdData = {"ru1801":[["9:00:00",1,2],["9:00:01",2,3],["9:00:03",1,4]],
	"rb1710":[["9:00:00",1,2],["9:00:01",2,3],["9:00:03",1,4]]}
