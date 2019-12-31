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


from fund_manage import fm
from fund_manage import fm2


Message = const.Message


class Money(fm2.Money):
  def __init__(self, fm, startMoney, code):
    # 像资金管理登记，告知本code希望的起始资金是多少
    self.__money = fm.Register(code, startMoney)
    self.__fm = fm
    self.__code = code
    self.moveList = []
  
  # 出金
  def withdraw(self, first):
    v1 = self.__fm.Alloc(self.__code, first)
    v2 = self.__money
    self.__money -= v2
    if v1 + v2 > 0:
      self.moveList.append(-(v1 + v2))
    return v1 + v2
  
  # 入金
  def deposit(self, v):
    self.__fm.Free(self.__code, v)
    self.moveList.append(v)
  
  @property
  def value(self):
    return self.__fm.Query(self.__code)

#########################################################
class FundManager:
  def __init__(self, stockSize):
    self.TOTALMONEY = 500000
    self.stockSize = stockSize
    
    self.totalMoney = self.TOTALMONEY
    self.MaxMoney = 0
    self.stockMap = {
    }  # 记录每个code借入和归还的资金
    self.eventCache = {}

  
  def Process(self, context, task):
    if task.key == Message.SUGGEST_BUY_EVENT:
      #缓存
      self.eventCache[context] = Task(
          Priority(
            Message.STAGE_BUY_TRADE, Message.PRIORITY_BUY),
          Message.BUY_EVENT, None, *task.args)
      # context.AddTask(
      #   Task(
      #     Priority(
      #       Message.STAGE_BUY_TRADE, Message.PRIORITY_BUY),
      #     Message.BUY_EVENT, None, *task.args))
  
  def Alloc(self, code, first):
    # first 表示是否是建仓，建仓考虑大宗资金分配，否则只考虑动用分红资金
    n = self.stockMap[code]['now']
    self.stockMap[code]['now'] = 0
    return n
  
  def Query(self, code):
    n = self.stockMap[code]['now']
    return n
  
  def Free(self, code, money):
    self.stockMap[code]['now'] += money
  
  def Register(self, code, money):
    self.stockMap[code] = {}
    self.stockMap[code]['start'] = money
    self.stockMap[code]['now'] = money
    return 0
  
  
  def StageChange(self, before):
    if not before:
      for k, v in self.eventCache.items():
        k.AddTask(v)
      self.eventCache = {}
