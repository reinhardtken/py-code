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
  
 
 #https://www.cnblogs.com/nxf-rabbit75/p/11111825.html
 
 
DIR_BUY = 1
DIR_NONE = 0
DIR_SELL = -1
HOLD_MONEY = 1
HOLD_STOCK = 2
BUY_PERCENT = 0.04
SELL_PERCENT = 0.03
 
  
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
    # self.money = 100000 #持币的时候，这个表示金额，持仓的的时候表示不够建仓的资金
    self.BEGIN_MONEY = 52105
    self.money = self.BEGIN_MONEY
    self.oldMoney = self.money
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
    self.MAXEND = self.Quater2Date(2099, 'first')#默认的冻结开仓截止日期
    self.holdStockDate = 0 #持股总交易天数
    self.holdStockNatureDate = 0 #持股总自然天数
    self.lastDate = None #最后回测的交易日
    self.lastPrice = 0 #最后回测的交易价格
    self.result = None #最后的交易结果

  def buyInner(self, price, money):
    #计算多少钱买多少股，返回股数，钱数
    number = money // (price * 100)
    restMoney = money - number * 100 * price
    return (number, restMoney)
  
  
  def Buy(self, date, triggerPrice, price, reason=''):
    try:
      if self.status == HOLD_MONEY:
        self.holdStockDate += 1
        
      #如果持币，以固定价格买入
      if price <= triggerPrice:
        if self.status == HOLD_MONEY:
          self.oldMoney = self.money
          nm = self.buyInner(price, self.money)
          self.number = nm[0]
          self.money = nm[1]
          #self.number = self.money // (price * 100)
          #self.money = self.money - self.number*100*price
          self.costPrice = price
          self.status = HOLD_STOCK

          # 记录
          mark = TradeMark()
          mark.reason('买入').date(date).dir(DIR_BUY).total(self.number * 100 * price).number(self.number).price(
            price).extraInfo(
            '{}'.format(reason)).Dump()
          self.tradeList.append(mark)
          # print("买入： 日期：{}, 触发价格：{}, 价格：{}, 数量：{}, 剩余资金：{}, 原因：{}".format(date, triggerPrice, price, self.number, self.money, reason))
        elif self.status == HOLD_STOCK:
          number, money = self.buyInner(price, self.money)
          if number > 0:
            #追加买入
            self.number += number
            self.money = money
            
            mark = TradeMark()
            mark.reason('追加买入').date(date).dir(DIR_BUY).total(self.number * 100 * price).number(self.number).price(
              price).extraInfo(
              '剩余资金：{}'.format(self.money)).Dump()
            self.tradeList.append(mark)
            # print("买入（追加买入）： 日期：{}, 触发价格：{}, 价格：{}, 追加数量：{}, 数量：{}, 剩余资金：{}, 原因：{}".format(date, triggerPrice, price,
            #                                                                                nm[0], self.number, self.money, reason))
    except Exception as e:
      print(e)
   
 
  def Sell(self, date, triggerPrice, price, reason=''):
    if price >= triggerPrice:
      self.SellNoCodition(date, triggerPrice, price, reason)
      
      
  def SellNoCodition(self, date, triggerPrice, price, reason=''):
    if self.status == HOLD_STOCK:
      self.money = self.money + self.number * 100 * price
      winLoss = (self.money - self.oldMoney) / self.oldMoney
      self.status = HOLD_MONEY

      # 记录
      mark = TradeMark()
      mark.reason('卖出').date(date).dir(DIR_SELL).total(self.number * 100 * price).number(self.number).price(price).extraInfo(
        '盈亏：{}, 原因：{}'.format(winLoss, reason)).Dump()
      self.tradeList.append(mark)
      # print(mark)
      # print("卖出： 日期：{}, 触发价格：{}, 价格：{}, 数量：{}, 盈亏：{}, 现金：{}, 原因：{}".format(date, triggerPrice, price,
      #                                                                      self.number, winLoss, self.money, reason))


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
          self.checkPoint[k+1]['buyPrice'] = v['year']['allDividend'] / BUY_PERCENT
          self.checkPoint[k + 1]['sellPrice'] = v['year']['allDividend'] / SELL_PERCENT
        else:
          self.checkPoint[k + 1]['buyPrice'] = -10000
          self.checkPoint[k + 1]['sellPrice'] = 10000
          
        # midYear的dividend影响8月31号以后的当年
        if v['midYear']['dividend'] > 0:
          self.checkPoint[k]['buyPrice2'] = v['midYear']['allDividend'] / BUY_PERCENT
          self.checkPoint[k]['sellPrice2'] = v['midYear']['allDividend'] / SELL_PERCENT
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
    
    #针对dangerousPoint清理dividendPoint
    tmp = []
    have = set()
    for one in self.dividendPoint:
      for two in self.dangerousPoint:
        if two[0] <= one[0] and two[1] >= one[0]:
          print("清理除权 {} {} {}".format(one[0], two[0], two[1]))
          break
      else:
        if one[0] not in have:
          tmp.append(one)
          have.add(one[0])
    self.dividendPoint = tmp
    
      


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
  
  
  def processSong(self, value):
    #处理送股
    index = value.find('送')
    if index != -1:
      newValue = value[index + 1:]
      out = util.String2Number(newValue)
      return out
    else:
      return 0
    
  def processPai(self, value):
    #处理派息
    index = value.find('派')
    if index != -1:
      newValue = value[index + 1:]
      out = util.String2Number(newValue)
      return out
    else:
      return 0
    
  def processPai2(self, value):
    #处理派息，税后
    index = value.find('扣税后')
    if index != -1:
      newValue = value[index + 1:]
      out = util.String2Number(newValue)
      return out
    else:
      return 0
  
  # def CalcDividend(self, year, position):
  #   #'10送3.00派4.00元(含税,扣税后3.30元)'
  #   if const.GPFH_KEYWORD.KEY_NAME['AllocationPlan'] in self.checkPoint[year][position]:
  #     value = self.checkPoint[year][position][const.GPFH_KEYWORD.KEY_NAME['AllocationPlan']]
  #     number = util.String2Number(value)
  #     index = value.find('派')
  #     if index != -1:
  #       newValue = value[index + 1:]
  #       profit = util.String2Number(newValue)
  #       self.checkPoint[year][position]['dividend'] = profit / number
  #       index2 = newValue.find('扣税后')
  #       if index2 != -1:
  #         newValue2 = newValue[index2 + 1:]
  #         profit2 = util.String2Number(newValue2)
  #         self.checkPoint[year][position]['dividend_aftertax'] = profit2 / number
  #
  #     if const.GPFH_KEYWORD.KEY_NAME['CQCXR'] in self.checkPoint[year][position]:
  #       self.dividendPoint.append((
  #         pd.to_datetime(np.datetime64(self.checkPoint[year][position][const.GPFH_KEYWORD.KEY_NAME['CQCXR']])),
  #         self.checkPoint[year][position]['dividend'], self.checkPoint[year][position]['dividend_aftertax']))

  def CalcDividend(self, year, position):
    # '10送3.00派4.00元(含税,扣税后3.30元)'
    if const.GPFH_KEYWORD.KEY_NAME['AllocationPlan'] in self.checkPoint[year][position]:
      value = self.checkPoint[year][position][const.GPFH_KEYWORD.KEY_NAME['AllocationPlan']]
      number = util.String2Number(value)
      profit = self.processPai(value)
      self.checkPoint[year][position]['dividend'] = profit / number
      profit2 = self.processPai2(value)
      self.checkPoint[year][position]['dividend_aftertax'] = profit2 / number
      gift = self.processSong(value)
      self.checkPoint[year][position]['gift'] = gift / number
    
      if const.GPFH_KEYWORD.KEY_NAME['CQCXR'] in self.checkPoint[year][position]:
        self.dividendPoint.append((
          pd.to_datetime(np.datetime64(self.checkPoint[year][position][const.GPFH_KEYWORD.KEY_NAME['CQCXR']])),
          self.checkPoint[year][position]['dividend'],
          self.checkPoint[year][position]['dividend_aftertax'],
          self.checkPoint[year][position]['gift']))
  
  def Quater2Date(self, year, quarter):
    #从某个季度，转换到具体日期
    if quarter == 'first':
      return pd.to_datetime(np.datetime64(str(year) + '-04-30T00:00:00Z'))
    elif quarter == 'second':
      return pd.to_datetime(np.datetime64(str(year) + '-08-31T00:00:00Z'))
    elif quarter == 'third':
      return pd.to_datetime(np.datetime64(str(year) + '-10-31T00:00:00Z'))
    elif quarter == 'forth':
      #来年一季度,这里反正有问题，用29号变通下
      return pd.to_datetime(np.datetime64(str(year+1) + '-04-29T00:00:00Z'))
  
  
  def ProcessQuarterPaper(self, year, position):
    if 'sjltz' in self.checkPoint[year][position]:
      speed = float(self.checkPoint[year][position]['sjltz'])
      if speed < -10:
        self.dangerousPoint.append((self.Quater2Date(year, position), self.MAXEND, year, position, speed))
      elif speed > 0:
        #增速转正，如果之前有负的，要结合负的计算出冷冻区间（此区间不开仓）
        if len(self.dangerousPoint) > 0:
          #找到所有没有填充终止的条目，全部填上当前时间点
          dirtyFlag = False
          for index in range(len(self.dangerousPoint)):
            if self.dangerousPoint[index][1] == self.MAXEND:
              dirtyFlag = True
              self.dangerousPoint[index] = (self.dangerousPoint[index][0], self.Quater2Date(year, position), self.dangerousPoint[index][2],
                                         self.dangerousPoint[index][3], self.dangerousPoint[index][4])
          
          #清理在起始时间小于终止时间的区间（比如从2011年2季度开始，2,3,4季度都是负，2012年一季度转正）
          #此时dangerousPoint里面有多个条目：（2011-2，2012-1），（2011-3，2012-1），（2011-4，2012-1）
          #其中（2011-3，2012-1），（2011-4，2012-1）是没有意义的，需要删除
          if dirtyFlag:
            tmp = []
            have = set()
            for index in range(len(self.dangerousPoint)):
              if self.dangerousPoint[index][1] not in have:
                have.add(self.dangerousPoint[index][1])
                tmp.append(self.dangerousPoint[index])
              else:
                pass
            self.dangerousPoint = tmp

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
    
  
  def ProcessDividend(self, date, buyPrice, price, dividend):
    if self.status == HOLD_STOCK:
      if buyPrice >= price:
        oldMoney = self.money
        oldNumber = self.number
        dividendMoney = self.number*100*dividend[2]
        money = dividendMoney+self.money
        number = money // (price * 100)
        self.money = money - number * 100 * price
        self.number += number
        
        #记录
        mark = TradeMark()
        mark.reason('除权买入').date(date).dir(DIR_BUY).total(number*100*price).number(number).\
          price(price).extraInfo('分红金额：{}'.format(dividendMoney)).Dump()
        self.tradeList.append(mark)
        # print(mark)
        # print("除权买入： 日期：{}, 除权日：{}, 触发价格：{}, 价格：{}, 数量：{}, 剩余资金：{}, 分红：{}".format(date, dividend[0], buyPrice, price, self.number, self.money,
        #                                                                   dividendMoney))
      else:
        oldMoney = self.money
        dividendMoney = self.number * 100 * dividend[2]
        self.money += dividendMoney
        # 记录
        mark = TradeMark()
        mark.reason('除权不买入').date(date).dir(DIR_NONE).total(dividendMoney).number(0).price(0).extraInfo(
          '分红金额：{}'.format(dividendMoney)).Dump()
        self.tradeList.append(mark)
        # print(mark)
        # print("除权不买入： 日期：{}, 除权日：{}, 触发价格：{}, 价格：{}, 数量：{}, 剩余资金：{}, 分红：{}".format(date, dividend[0], buyPrice, price, self.number, self.money,
        #                                                               dividendMoney))
  
  
  def MakeDecisionPrice(self, date):
    #决定使用哪个年的checkpoit，返回对应的buy和sell

    #在4月30日之前，只能使用去年的半年报，如果半年报没有，则无法交易
    anchor0 = pd.Timestamp(datetime(date.year, 4, 30))
    #在8月31日之前，需要使用去年的年报和半年报
    anchor1 = pd.Timestamp(datetime(date.year, 8, 31))
    
    if date <= anchor0:
      if self.checkPoint[date.year]['buyPrice'] > 0:
        return True, self.checkPoint[date.year]['buyPrice'], self.checkPoint[date.year]['sellPrice']
    elif date <= anchor1:
      if self.checkPoint[date.year]['buyPrice'] > 0:
        return True, self.checkPoint[date.year]['buyPrice'], self.checkPoint[date.year]['sellPrice']
    else:
      #使用去年的allDividend和半年报中dividend中大的那个决定
      buy = self.checkPoint[date.year]['buyPrice']
      midBuy = self.checkPoint[date.year]['buyPrice2']
      if buy > midBuy:
        return True, buy, self.checkPoint[date.year]['sellPrice']
      else:
        if midBuy > 0:
          return True, midBuy, self.checkPoint[date.year]['sellPrice2']
      
    return False, 0, 0
  

  
    
    
  def BackTest(self):
    #回测
    cooldown = False
    cooldownEnd = None
    for date, row in self.data.iterrows():
      try:
        if cooldown:
          if date >= cooldownEnd:
            cooldown = False
            print('cooldownend {}'.format(cooldownEnd))
            cooldownEnd = None
          else:
            continue
            
        #midYear, year = self.MakeDecisionYear(date)
        year = date.year
        self.lastDate = date
        self.lastPrice = row['close']
        
        action, buyPrice, sellPrice = self.MakeDecisionPrice(date)
        if action:
          self.Buy(date, buyPrice, row['close'], reason='低于买点')
          self.Sell(date, sellPrice, row['close'], reason='高于卖点')
          
          
          #处理除权,
          # 除权日不可能不是交易日
          if len(self.dividendPoint) > 0 and date == self.dividendPoint[0][0]:
            self.ProcessDividend(date, buyPrice, row['close'], self.dividendPoint[0])
            self.dividendPoint = self.dividendPoint[1:]
          
          #处理季报，检查是否扣非-10%
          if len(self.dangerousPoint) >0 and date >= self.dangerousPoint[0][0]:
            self.SellNoCodition(date, sellPrice, row['close'], reason='扣非卖出: {}'.format(self.dangerousPoint[0][4]))
            #记录因为扣非为负的区间，在区间内屏蔽开仓
            cooldown = True
            cooldownEnd = self.dangerousPoint[0][1]
            self.dangerousPoint = self.dangerousPoint[1:]
  
      except TypeError as e:
        print(e)
      except KeyError as e:
        print(e)



  def CloseAccount(self):
    if self.status == HOLD_MONEY:
      profit, profitPercent = self.CloseAccountHoldMoney()
      self.result = "结算(持币)： 日期：{}, 终止资金：{}, 开始资金：{}, 收益：{}, 收益率：{}, 持有天数：{}".format(self.lastDate, self.money, self.BEGIN_MONEY, profit,
                                                                                 profitPercent, self.holdStockDate)
    elif self.status == HOLD_STOCK:
      self.money = self.lastPrice*self.number*100
      profit, profitPercent = self.CloseAccountHoldMoney()
      self.result = "结算(持股)： 日期：{}, 终止资金：{}, 开始资金：{}, 收益：{}, 收益率：{}, 持有天数：{}, 持股数：{}".format(self.lastDate, self.money, self.BEGIN_MONEY,
                                                                         profit,
                                                                         profitPercent, self.holdStockDate, self.number)
    
    print(self.result)
  
  
  
  def CloseAccountHoldMoney(self):
    profit = self.money - self.BEGIN_MONEY
    profitPercent = profit / self.BEGIN_MONEY
    return profit, profitPercent
  
  
  def Store2DB(self):
    #保存交易记录到db，用于回测验证
    out = {"_id": self.code}
    out["beginMoney"] = self.BEGIN_MONEY
    tl = []
    for one in self.tradeList:
      tl.append(one.ToDB())
    out['tradeMarks'] = tl
    out['result'] = self.result
    util.SaveMongoDB(out, 'stock_backtest', 'dv1')
    
  def CheckResult(self):
    db = self.mongoClient["stock_backtest"]
    collection = db['dv1']
    cursor = collection.find({"_id": self.code})
    out = None
    for c in cursor:
      out = c
      break
    
    if self.BEGIN_MONEY == out['beginMoney']:
      if len(self.tradeList) == len(out['tradeMarks']):
        if self.result == out['result']:
          for index in range(len(self.tradeList)):
            if self.tradeList[index] != TradeMark.FromDB(out['tradeMarks'][index]):
              return False
          else:
            return True
    
    return False

    
      
#交易记录
class TradeMark:
  def __init__(self):
    self.__date = None #交易发生的时间
    self.__dir = None #交易发生的方向，1 买入，-1 卖出
    self.__fee = None
    self.__number = None #股票交易数量
    self.__price = None #股票交易的金额
    self.__total = None #涉及的总金额
    self.__reason = None #交易原因
    self.__extraInfo = None #其他附带信息
 
  def date(self, d):
    self.__date = d
    return self
  
  def dir(self, d):
    self.__dir = d
    return self
  
  def fee(self, d):
    self.__fee = d
    return self
  
  def number(self, d):
    self.__number = d
    return self
  
  def price(self, d):
    self.__price = d
    return self
  
  def total(self, d):
    self.__total = d
    return self
  
  def reason(self, d):
    self.__reason = d
    return self
  
  def extraInfo(self, d):
    self.__extraInfo = d
    return self
  
  def Dump(self):
    print(self)
    
  def ToDB(self):
    return { 'op': self.__reason, 'date':self.__date, 'dir':self.__dir, 'total':self.__total, 'number':self.__number, 'price':self.__price,
      'extraInfo': self.__extraInfo }
  
  def FromDB(db):
    one = TradeMark()
    one.reason(db['op']).date(db['date']).dir(db['dir']).total(db['total']).number(db['number']).price(db['price']).extraInfo(db['extraInfo'])
    return one
  
  def __str__(self):
    return "操作：{}, 日期：{}, 方向：{}, 金额：{}, 价格：{}, 数量：{}, 附加信息：{}, ".format(
      self.__reason, self.__date, self.__dir, self.__total, self.__price, self.__number, self.__extraInfo)
  
  def __eq__(self, obj):
    return self.__reason == obj.__reason and self.__date == obj.__date and self.__dir == obj.__dir \
      and self.__total == obj.__total and self.__price == obj.__price and self.__number == obj.__number \
      and self.__fee == obj.__fee and self.__extraInfo == obj.__extraInfo

def Test2(code, save=False, check=False):
  stock = TradeUnit()
  stock.code = code
  stock.LoadQuotations()
  stock.CheckPrepare()

  print(stock.checkPoint)
  print(stock.dangerousPoint)
  print(stock.dividendPoint)
  
  stock.BackTest()
  stock.CloseAccount()
  if save:
    stock.Store2DB()
    
  if check:
    assert stock.CheckResult()
  print(stock.checkPoint)
  print(stock.dangerousPoint)
  print(stock.dividendPoint)
  
        
        
if __name__ == '__main__':
  #皖通高速
  Test2('600012', False, True)
  #万华化学
  # Test2('600309')