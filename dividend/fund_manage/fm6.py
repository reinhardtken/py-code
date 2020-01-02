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

Message = const.Message

#代表一次交易
class Move:
  def __init__(self, code, name, date, days, change, old, winLoss):
    self.code = code
    self.name = name
    self.date = date
    self.old = old
    self.change = change
    self.winLoss = winLoss
    self.days = int(days)
    
    
  
  def __str__(self):
    info = '### FundManager:Move {} {}, {} {}天, {:.2f}, {:.2f}, {:.2f}'.format(self.code, self.name,
                                                                          self.date, self.days, self.winLoss,
                                                                           self.old,
                                                                           self.change)
    return info


  def __lt__(self, other):
    return self.winLoss < other.winLoss
#########################################################
# 每份5万元，不限制份数。如果单前份数用光，则申请新份数
# 1 对于总计赚钱的股票，总是追加这个股曾经归还的最大额资金（马太效应）
# 2 对于总计亏钱的股票，总是追加这个股曾经归还的最大额资金（避免持续亏损）
# 3 对于1和2，不得超过总本金的20%

#在对比了fm5和fm6的move数据后，fm6显然收益的合理性比fm5高很多
#fm5：
### win movelist ###
### FundManager:Move 000651 2016-05-03 00:00:00, 2275470.00, 1512185.86, 3787655.86
### FundManager:Move 600741 2013-05-02 00:00:00, 404451.60, 491102.82, 895554.42
### FundManager:Move 601009 2018-05-02 00:00:00, 400100.01, 3559283.58, 3959383.59
### FundManager:Move 600900 2017-05-02 00:00:00, 298241.10, 685342.82, 983583.92
### FundManager:Move 000333 2014-04-30 00:00:00, 238112.00, 388435.57, 626547.57
### loss movelist ###
### FundManager:Move 000651 2015-05-04 00:00:00, -600576.00, 2209783.82, 1609207.82
### FundManager:Move 600660 2011-03-21 00:00:00, -121869.60, 500000.00, 378130.40
### FundManager:Move 601818 2015-07-30 00:00:00, -79489.80, 651397.86, 571908.06
### FundManager:Move 601515 2019-04-23 00:00:00, -61852.00, 192003.70, 130151.70
### FundManager:Move 600809 2013-09-18 00:00:00, -45066.00, 174282.57, 129216.57
#fm6：
### win movelist ###
### FundManager:Move 000651 2016-05-03 00:00:00, 133170.00, 89169.00, 222339.00
### FundManager:Move 600741 2016-05-03 00:00:00, 97275.20, 132766.00, 230041.20
### FundManager:Move 600660 2013-05-02 00:00:00, 94829.00, 38052.00, 132881.00
### FundManager:Move 601818 2014-05-05 00:00:00, 90570.64, 51615.14, 142185.78
### FundManager:Move 600036 2013-05-02 00:00:00, 90145.50, 69747.00, 159892.50
### loss movelist ###
### FundManager:Move 000651 2015-05-04 00:00:00, -32256.00, 121425.00, 89169.00
### FundManager:Move 600027 2015-08-25 00:00:00, -29200.00, 185818.75, 156618.75
### FundManager:Move 000981 2018-06-19 00:00:00, -29043.00, 50000.00, 20957.00
### FundManager:Move 002269 2012-07-09 00:00:00, -24564.00, 50000.00, 25436.00
### FundManager:Move 300134 2011-09-05 00:00:00, -21060.00, 50000.00, 28940.00
class FundManager:
  def __init__(self, stocks, tm, startDate, endDate):
    self.TOTALMONEY = 500000
    self.perShare = 50000
    # self.nowMax = self.TOTALMONEY / self.perShare
    self.stocks = stocks
    self.code2Name = {}
    for one in stocks:
      self.code2Name[one['_id']] = one['name']
    self.stockSize = len(stocks)
    self.startDate = startDate
    self.endDate = endDate
    self.TM = tm
    
    self.totalMoney = self.TOTALMONEY
    self.MaxMoney = 0
    self.stockMap = {}
    for one in stocks:
      self.stockMap[one['_id']] = {}
      self.stockMap[one['_id']]['allWinLoss'] = 0
    self.stockNowMap = {
    }  # 记录每个code借出的资金
    self.stockSet = set()
    self.stockNowSet = set()  # 当前持有的股票
    self.eventCache = {}
    self.moveList = []
    self.lastPayback = {}  # 个股计算盈亏的时候，需要最后一次归还的资金
    self.lastDate = None
    
    dfIndex = pd.date_range(start=startDate, end=endDate, freq='M')
    self.df = pd.DataFrame(np.random.randn(len(dfIndex)), index=dfIndex, columns=['willDrop'])
    self.df = pd.concat([self.df, pd.DataFrame(columns=[
      'total', 'capital', 'profit', 'percent',
      # 'utilization',
      'cash', 'marketValue', 'stockNumber'
    ])], sort=False)
    self.df.drop(['willDrop', ], axis=1, inplace=True)
    
    self.quarterDetail = {}
  
  def Process(self, context, task):
    if task.key == Message.SUGGEST_BUY_EVENT:
      # 缓存
      self.eventCache[context] = Task(
        Priority(
          Message.STAGE_BUY_TRADE, Message.PRIORITY_BUY),
        Message.BUY_EVENT, None, *task.args)
      # context.AddTask(
      #   Task(
      #     Priority(
      #       Message.STAGE_BUY_TRADE, Message.PRIORITY_BUY),
      #     Message.BUY_EVENT, None, *task.args))
    elif task.key == Message.OTHER_WORK:
      if context.date in self.df.index:
        # 计算月度终值
        digest, detail = self.TM.CalcNowValue()
        self.df.loc[context.date, 'cash'] = self.totalMoney
        self.df.loc[context.date, 'capital'] = self.TOTALMONEY
        self.df.loc[context.date, 'marketValue'] = digest['marketValue']
        self.df.loc[context.date, 'stockNumber'] = digest['stockNumber']
        self.df.loc[context.date, 'total'] = self.totalMoney + digest['marketValue']
        self.df.loc[context.date, 'profit'] = self.df.loc[context.date, 'total'] - self.TOTALMONEY
        self.df.loc[context.date, 'percent'] = self.df.loc[context.date, 'profit'] / self.TOTALMONEY
        # self.df.loc[context.date, 'utilization'] = len(self.stockNowSet) / self.nowMax
        self.quarterDetail[context.date] = detail
        pass
    elif task.key == Message.NEW_DAY:
      self.lastDate = context.date
  
  def Alloc(self, code, first):
    # first 表示是否是建仓，建仓考虑大宗资金分配，否则只考虑动用分红资金
    n = 0
    if code in self.stockNowMap:
      n = self.stockNowMap[code]['total']
      self.stockNowMap[code]['old'] = n
      self.stockNowMap[code]['total'] = 0
    
    if n > 0:
      info = '### FundManager alloc {} {:.2f}'.format(code, n)
      # self.moveList.append(info)
      print(info)
    return n
  
  def Query(self, code):
    n = 0
    if code in self.stockNowMap:
      n = self.stockNowMap[code]['change']
    elif code in self.lastPayback:
      n = self.lastPayback[code]
    return n
  
  def Free(self, code, money, paybackAll):
    self.totalMoney += money
    self.stockNowMap[code]['change'] += money
    info = '### FundManager free {} {:.2f}, {:.2f}'.format(code, money, self.totalMoney)
    #self.moveList.append(info)
    print(info)
    if paybackAll:
      self.lastPayback[code] = self.stockNowMap[code]['change']
      winLoss = self.stockNowMap[code]['change'] - self.stockNowMap[code]['old']
      diff = self.lastDate - self.stockNowMap[code]['date']
      move = Move(code, self.code2Name[code], self.stockNowMap[code]['date'], diff.days,
                  self.stockNowMap[code]['change'],
           self.stockNowMap[code]['old'], winLoss)
      print(move)
      
      self.stockMap[code]['lastWinLoss'] = winLoss
      #记录在这个股票上的得失
      self.stockMap[code]['allWinLoss'] += winLoss
      self.stockMap[code]['old'] = self.stockNowMap[code]['change']
      self.moveList.append(move)
      print(info)
      self.stockNowMap.pop(code)
      self.stockNowSet.discard(code)
  
  def Register(self, code, money):
    # self.stockNowMap[code] = {}
    # self.stockNowMap[code]['start'] = money
    # self.stockNowMap[code]['now'] = money
    return 0
  
  def StageChange(self, before):
    if not before:
      # 统计买入信号和持股的差，计算总的资金需求量
      request = set()
      for k, v in self.eventCache.items():
        request.add(k.code)
      
      diff = request - self.stockNowSet
      
      if len(diff) > 0:
        # 计算需要的资金总量
        requestMoneyTotal = 0
        requestMoneyMap = {}
        for code in diff:
          if self.stockMap[code]['allWinLoss'] > 0:
            tmp = self.stockMap[code]['old']
            #单支股票不能超过总额度20%
            if tmp > self.TOTALMONEY*0.2:
              tmp = self.TOTALMONEY*0.2
            requestMoneyTotal += tmp
            requestMoneyMap[code] = tmp
          elif self.stockMap[code]['allWinLoss'] == 0:
            requestMoneyTotal += self.perShare
            requestMoneyMap[code] = self.perShare
          else:
            requestMoneyTotal += self.stockMap[code]['old']
            requestMoneyMap[code] = self.stockMap[code]['old']
  
        if self.totalMoney >= requestMoneyTotal:
          pass
        else:
          n = (requestMoneyTotal - self.totalMoney) // self.perShare + 1
          print('### money is not enough {} {} {}'.format(requestMoneyTotal, self.totalMoney, n))
          self.TOTALMONEY += self.perShare * n
          self.totalMoney += self.perShare * n
          
        counter = 0
        for k, v in self.eventCache.items():
          # 如果买入信号的股票没有持仓
          if k.code in diff:
            print('### FundManager alloc all {} {}'.format(k.code, requestMoneyMap[k.code]))
            self.stockNowMap[k.code] = {}
            self.stockNowMap[k.code]['total'] = requestMoneyMap[k.code]
            self.stockNowMap[k.code]['change'] = 0
            self.stockNowMap[k.code]['date'] = k.date
            self.stockSet.add(k.code)
            self.stockNowSet.add(k.code)
            self.totalMoney -= requestMoneyMap[k.code]
            counter += 1
            k.AddTask(v)
            if counter == len(diff):
              break
      self.eventCache = {}
