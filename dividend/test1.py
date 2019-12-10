# -*- coding: utf-8 -*-

# sys
from datetime import datetime
from dateutil import parser

# thirdpart
import pandas as pd
from pymongo import MongoClient
import numpy as np


import const
import util

# this project
if __name__ == '__main__':
  import sys
  
  
DIR_BUY = 1
DIR_SELL = -1
HOLD_MONEY = 1
HOLD_STOCK = 2
 
  
#尝试计算股息，根据股息买卖股的收益
def Test(code):
  client = MongoClient()
  db = client['stock2']
  collection = db['dv']
  
  out = []
  totalMoney = 100000
  stockNumber = 0
  cashOrStock = 0 # 0 cash 1 stock
  cursor = collection.find({"_id": code})
  index = 0
  flag = False
  for c in cursor:
    date = c["date"]
    allPrice = c["price"]
    dv = c["dv"]
    
  for index in range(len(date)):
    if flag is False and date[index].startswith("2011-"):
      flag = True
      
    if flag:
      if cashOrStock == 0 and dv[index] >= 4.0:
        #买入
        price = float(allPrice[index])
        stockNumber = totalMoney / price
        print("buy action price {}, dv {}, and number {}".format(price, dv[index], stockNumber))
        cashOrStock = 1
      elif cashOrStock == 1 and dv[index] <= 3.0:
        #卖出
        price = float(allPrice[index])
        totalMoney = stockNumber * price
        print("sell action price {}, dv {}, and money {}".format(price, dv[index], totalMoney))
        cashOrStock = 0
  
  if cashOrStock == 0:
    print("final result {}".format(totalMoney))
  else:
    print("final result2 {}".format(stockNumber*float(allPrice[-1])))
    
    

class TradeUnit:
  #代表一个交易单元，比如10万本金
  def __init__(self):
    self.tradeList = []#交易记录
    self.status = HOLD_MONEY#持仓还是持币
    self.money = 100000 #持币的时候，这个表示金额，持仓的的时候表示不够建仓的资金
    self.costPrice = 0 #持仓的时候，表示持仓成本
    self.number = 0 #持仓的时候表示持仓数目(手)
    self.startYear = 2011 #起始年份
    self.checkYear = self.startYear
    self.checkPoint = {}#所有的年报季报除权等影响买卖点的特殊时点
    self.code = None#代码
    self.mongoClient = MongoClient()
    self.dangerousPoint = []#利润同比下滑超过10%的位置
    self.dividendPoint = []  # 除权的日期
    self.data = None #行情

  def Buy(self, date, triggerPrice, price):
    #如果持币，以固定价格买入
    oldMoney = self.money
    if self.status == HOLD_MONEY:
      self.number = self.money // (price * 100)
      self.money = self.money - self.number*100*price
      self.costPrice = price
      self.status = HOLD_STOCK
      print("买入： 日期：{}, 触发价格：{}, 价格：{}, 数量：{}, 剩余资金：{}".format(date, triggerPrice, price, self.number, self.money))
    
      
   
 
  def Sell(self, date, triggerPrice, price):
    if self.status == HOLD_STOCK:
      self.money = self.money + self.number*100*price
      self.status = HOLD_MONEY
      print("卖入： 日期：{}, 触发价格：{}, 价格：{}, 数量：{}".format(date, triggerPrice, price, self.number))



  def CheckPrepare(self):
    #准备判定条件
    now = datetime.now()
    stopYear = now.year
    for year in range(self.startYear-1, stopYear+1):
      if year not in self.checkPoint:
        self.checkPoint[year] = {}
      if year+1 not in self.checkPoint:
        self.checkPoint[year+1] = {}
      #加载对应年的年报中报
      yearPaper = self.LoadYearPaper(year)
      self.checkPoint[year]['midYear'] = yearPaper[0]
      self.checkPoint[year]['year'] = yearPaper[1]
      
      #加载对应的季报
      quarterPaper = self.LoadQuaterPaper(year)
      self.checkPoint[year]['first'] = quarterPaper[0]
      self.checkPoint[year]['second'] = quarterPaper[1]
      self.checkPoint[year]['third'] = quarterPaper[2]
      self.checkPoint[year]['forth'] = quarterPaper[3]
    
    #对加载出来的数据做初步处理
    for k, v in self.checkPoint.items():
      try:
        #计算分红
        v['midYear']['dividend'] = 0
        v['year']['dividend'] = 0
        self.CalcDividend(k, 'midYear')
        self.CalcDividend(k, 'year')
        v['year']['allDividend'] = v['midYear']['dividend'] + v['year']['dividend']
        
        #根据分红计算全年和半年的买入卖出价格
        #allDividend影响下一年
        if v['year']['allDividend'] > 0:
          self.checkPoint[k+1]['buyPrice'] = v['year']['allDividend'] / 0.04
          self.checkPoint[k + 1]['sellPrice'] = v['year']['allDividend'] / 0.03
        else:
          self.checkPoint[k + 1]['buyPrice'] = -10000
          self.checkPoint[k + 1]['sellPrice'] = 10000
          
        # midYear的dividend影响8月31号以后的当年
        if v['midYear']['dividend'] > 0:
          self.checkPoint[k]['buyPrice2'] = v['midYear']['allDividend'] / 0.04
          self.checkPoint[k]['sellPrice2'] = v['midYear']['allDividend'] / 0.03
        else:
          self.checkPoint[k]['buyPrice2'] = -10000
          self.checkPoint[k]['sellPrice2'] = 10000
          
        #检查净利润同比下降10%以上的位置
        self.ProcessQuarterPaper(k, 'first')
        self.ProcessQuarterPaper(k, 'second')
        self.ProcessQuarterPaper(k, 'third')
        self.ProcessQuarterPaper(k, 'forth')
      except KeyError as e:
        print(e)
      


  def LoadYearPaper(self, y):
    #加载年报，中报
    midYear = {}
    year = {}
    db = self.mongoClient["stock"]
    collection = db["gpfh-"+str(y)+"-06-30"]
    cursor = collection.find({"_id": self.code})
    for c in cursor:
      midYear[const.GPFH_KEYWORD.KEY_NAME['CQCXR']] = c[const.GPFH_KEYWORD.KEY_NAME['CQCXR']]
      midYear[const.GPFH_KEYWORD.KEY_NAME['AllocationPlan']] = c[const.GPFH_KEYWORD.KEY_NAME['AllocationPlan']]
      break

    collection = db["gpfh-" + str(y) + "-12-31"]
    cursor = collection.find({"_id": self.code})
    for c in cursor:
      year[const.GPFH_KEYWORD.KEY_NAME['CQCXR']] = c[const.GPFH_KEYWORD.KEY_NAME['CQCXR']]
      year[const.GPFH_KEYWORD.KEY_NAME['AllocationPlan']] = c[const.GPFH_KEYWORD.KEY_NAME['AllocationPlan']]
      break
      
    return (midYear, year)
  
  
  def LoadQuaterPaper(self, year):
    #加载季报
    first = {}
    second = {}
    third = {}
    forth = {}
    db = self.mongoClient["stock"]
    collection = db["yjbg-" + self.code]
    strYear = str(year)
    #一季度
    cursor = collection.find({"_id": strYear+"-03-31"})
    for c in cursor:
      first['sjltz'] = c['sjltz']
      break

    # 二季度
    cursor = collection.find({"_id": strYear+"-06-30"})
    for c in cursor:
      second['sjltz'] = c['sjltz']
      break

    # 三季度
    cursor = collection.find({"_id": strYear + "-09-30"})
    for c in cursor:
      third['sjltz'] = c['sjltz']
      break

    # 四季度
    cursor = collection.find({"_id": strYear + "-12-31"})
    for c in cursor:
      forth['sjltz'] = c['sjltz']
      break

    return (first, second, third, forth)
  
  
  def CalcDividend(self, year, position):
    if const.GPFH_KEYWORD.KEY_NAME['AllocationPlan'] in self.checkPoint[year][position]:
      value = self.checkPoint[year][position][const.GPFH_KEYWORD.KEY_NAME['AllocationPlan']]
      number = util.String2Number(value)
      index = value.find('派')
      if index != -1:
        newValue = value[index + 1:]
        profit = util.String2Number(newValue)
        self.checkPoint[year][position]['dividend'] = profit / number
        
      if const.GPFH_KEYWORD.KEY_NAME['CQCXR'] in self.checkPoint[year][position]:
        self.dividendPoint.append((
          np.datetime64(self.checkPoint[year][position][const.GPFH_KEYWORD.KEY_NAME['CQCXR']]), self.checkPoint[year][position]['dividend']))
    
  
  
  def Quater2Date(self, year, quarter):
    #从某个季度，转换到具体日期
    if quarter == 'first':
      return np.datetime64(str(year) + '-04-30')
    elif quarter == 'second':
      return np.datetime64(str(year) + '-08-31')
    elif quarter == 'third':
      return np.datetime64(str(year) + '-10-31')
    elif quarter == 'forth':
      #来年一季度,这里反正有问题，用29号变通下
      return np.datetime64(str(year+1) + '-04-29')
  
  
  def ProcessQuarterPaper(self, year, position):
    if 'sjltz' in self.checkPoint[year][position]:
      speed = float(self.checkPoint[year][position]['sjltz'])
      if speed < -10:
        self.dangerousPoint.append((self.Quater2Date(year, position), year, position, speed))


  def LoadQuotations(self):
    db = self.mongoClient["stock_all_kdata_none"]
    collection = db[self.code]
    start = str(self.startYear)+'-01-01T00:00:00Z'
    datetime1 = parser.parse(start)
    cursor = collection.find({"_id": {"$gte": datetime1}})
    out = []
    for c in cursor:
      out.append(c)
  
    if len(out):
      df = pd.DataFrame(out)
      df.set_index('_id', inplace=True)
      
    self.data = df
    
  
  def BackTest(self):
    #回测
    for date, row in self.data.iterrows():
      try:
        year = date.year
        if year in self.checkPoint:
          cp = self.checkPoint[year]
          #先完全忽略半年报
          if row['close'] < cp['buyPrice']:
            self.Buy(date, cp['buyPrice'], row['close'])
          elif row['close'] > cp['sellPrice']:
            self.Sell(date, cp['sellPrice'], row['close'])
  
      except TypeError as e:
        print(e)
      except KeyError as e:
        print(e)
    
      

class TradeMark:
  def __init__(self):
    self.date = None #交易发生的时间
    self.dir = None #交易发生的方向，1 买入，-1 卖出
    self.fee = None
    self.number = None #股票交易数量
    self.price = None
    self.total = None
 


def Test2(code):
  stock = TradeUnit()
  stock.code = code
  stock.LoadQuotations()
  stock.CheckPrepare()

  print(stock.checkPoint)
  print(stock.dangerousPoint)
  print(stock.dividendPoint)
  
  stock.BackTest()
  print(stock.checkPoint)
  print(stock.dangerousPoint)
  print(stock.dividendPoint)
  
        
        
if __name__ == '__main__':
  # Test("sh600012")
  # Test("sh600309")
  Test2('600012')