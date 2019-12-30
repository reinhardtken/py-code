# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from dateutil import parser
from pytz import timezone
import traceback
from queue import PriorityQueue

# thirdpart
import pandas as pd
from pymongo import MongoClient
import numpy as np

import const
import util

from comm import TradeResult
from comm import TradeMark
from comm import Pump
from comm import Retracement
from comm import MaxRecord
from comm import Priority
from comm import Task


class Money:
  pass


class FundManager:
  def __init__(self, stockSize):
    self.TOTALMONEY = 500000
    self.stockSize = stockSize
    
    self.totalMoney = self.TOTALMONEY
    self.MaxMoney = 0
    self.stockMap = {}  # 记录每个code借入和归还的资金
  
  def AfterSellStage(self, stage):
    # 在这里做资金管理后再真正转发
    pass
  
  def Alloc(self, code, money):
    self.totalMoney -= money
    if self.MaxMoney < abs(self.totalMoney) and self.totalMoney < 0:
      self.MaxMoney = abs(self.totalMoney)
      print('###FundManager: new Max Money {} ###'.format(self.MaxMoney))
    
    print('###FundManager: alloc {} {} {}###'.format(code, money, self.totalMoney))
    pass
  
  def Free(self, code, money):
    self.totalMoney += money
    print('###FundManager: free {} {} {}###'.format(code, money, self.totalMoney))
    pass