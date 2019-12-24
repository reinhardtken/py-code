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
  
 
#########################################################
def TestOne(code, beginMoney, name, save=False, check=False):
  import strategy.dv1
  stock = strategy.dv1.TradeUnit(code, name, beginMoney)
  stock.LoadQuotations()
  stock.LoadIndexs()
  stock.Merge()
  stock.CheckPrepare()

  print(stock.DV.checkPoint)
  print(stock.DV.dangerousPoint)
  for one in stock.DV.dividendPoint:
    print(one)
  
  stock.BackTest()
  stock.CloseAccount()
  if save:
    stock.Store2DB()
    
  if check:
    assert stock.CheckResult()
  # print(stock.checkPoint)
  # print(stock.dangerousPoint)
  # print(stock.dividendPoint)
  return stock


def TestTwo(codes, beginMoney, args):
  import strategy.dv2
  
  stock = strategy.dv2.TradeManager(codes, beginMoney)
  stock.LoadQuotations()
  stock.LoadIndexs()
  stock.Merge()
  stock.CheckPrepare()
  
  if 'saveprepare' in args:
    stock.StorePrepare2DB()
    
  if 'backtest' in args:
    stock.BackTest()
    stock.CloseAccount()
    
  if 'save' in args:
    stock.StoreResult2DB()
  
  if 'check' in args:
    assert stock.CheckResult()
  # print(stock.checkPoint)
  # print(stock.dangerousPoint)
  # print(stock.dividendPoint)
  return stock



def TestAll(codes, save, check):
  # # 皖通高速
  # TestOne('600012', 52105, save, check)
  # # 万华化学
  # TestOne('600309', 146005, save, check)
  # # 北京银行
  # TestOne('601169', 88305, save, check)
  # # 大秦铁路
  # # 2015年4月27日那天，预警价为14.33元，但收盘价只有14.32元，我们按照收盘价计算，
  # # 差一分钱才触发卖出规则。如果当时卖出，可收回现金14.32*12500+330=179330元。
  # # 错过这次卖出机会后不久，牛市见顶，股价狂泻，从14元多一直跌到5.98元。
  # # TODO 需要牛市清盘卖出策略辅助
  # TestOne('601006', 84305, save, check)
  # # 南京银行
  # TestOne('601009', 75005, save, check)
  for one in codes:
    if len(one) == 3:
      TestOne(one['code'], one['money'], one['name'], save, check)
    else:
      TestOne(one['code'], 100000, one['name'], save, check)
    


  
    
def CompareOne(code, name):
  client = MongoClient()
  db = client["stock_backtest"]
  collection = db["dv1"]
  cursor = collection.find({"_id": code})
  out = None
  for c in cursor:
    out = c
    break
  
  if out is not None:
    result = {'code': code, 'name': name}
    result['profit'] = out['result']['percent']
    result['hs300Profit'] = out['result']['hs300Profit']
    result['winHS300'] = result['profit'] - result['hs300Profit']
    return result
    

def CompareAll(codes):
  out = []
  TOTAL = len(codes)
  winNumber = 0
  allHS300Profit = 0
  allProfit = 0
  holdAllTimeHS300 = 0
  HOLD_ALL_HS300_PROFIT = 0.24
  for one in codes:
    tmp = CompareOne(one['code'], one['name'])
    holdAllTimeHS300 += HOLD_ALL_HS300_PROFIT
    if tmp['winHS300'] > 0:
      winNumber += 1
      allHS300Profit += tmp['hs300Profit']
      allProfit += tmp['profit']
    out.append(tmp)

  out.sort(key=lambda x: x['profit'])
  out.reverse()
  print("{}, {}, {}, {}, {}".format(winNumber, TOTAL, allProfit, allHS300Profit, holdAllTimeHS300))
  for one in out:
    print(one)
  


def TestBank():
  # 从所有的符合条件的银行股里面，判断最近是否符合买入卖出条件
  # 1 更新行情数据
  
  # 2回测
  client = MongoClient()
  db = client["stock_backtest"]
  collection = db["all_dv1_digest"]
  cursor = collection.find({'name': {'$regex': '银行', }})
  out = []
  for c in cursor:
    out.append(c)

  strategy.dv1.SignalDV(out)


def SignalAll():
  # 从所有的符合条件的银行股里面，判断最近是否符合买入卖出条件
  # 1 更新行情数据
  
  # 2回测
  client = MongoClient()
  db = client["stock_backtest"]
  collection = db["all_dv1_digest"]
  cursor = collection.find()
  out = []
  for c in cursor:
    out.append(c)
  
  strategy.dv1.SignalDV(out)


def CalcDVAll():
  client = MongoClient()
  db = client["stock_backtest"]
  collection = db["all_dv1_digest"]
  cursor = collection.find()
  out = []
  for c in cursor:
    out.append(c)
  
  strategy.dv1.CalcDV(out)
  


def HoldAll():
  client = MongoClient()
  db = client["stock_backtest"]
  collection = db["all_dv1"]
  cursor = collection.find({'status': 2})
  out = []
  for c in cursor:
    out.append(c)
  
  strategy.dv1.HoldDV(out)
  



def TestA():
  df1 = util.LoadData('stock_signal', '2019-12-21', condition={'操作': 1}, sort=[('百分比', -1)])
  df2 = util.LoadData('stock_statistcs', 'dvYears', condition={}, sort=[('百分比', -1)])
  
  mergeData = df1.join(df2, how='left', rsuffix='right')
  codes = []
  for code, row in mergeData.iterrows():
    codes.append(code)
  df3 = util.LoadData2('stock_backtest', 'all_dv1_digest', codes)
  df4 = util.LoadData2('stock_statistcs', 'quarterSpeed', codes)
  df5 = util.LoadData2('stock', 'stock_list', codes)
  df6 = util.LastPriceNone(codes)
  df5 = df5[['所属行业', '地区', '总股本(亿)']]
  mergeData = mergeData.join(df3, how='left', rsuffix='right2')
  mergeData = mergeData.join(df4, how='left', rsuffix='right3')
  mergeData = mergeData.join(df5, how='left', rsuffix='right4')
  mergeData = mergeData.join(df6, how='left', rsuffix='right5')
  mergeData['总市值(亿)'] = mergeData['price']*mergeData['总股本(亿)']
  # mergeData.eval('总市值 = price * 总股本(亿)', inplace=True)
  mergeData.to_excel("c:/workspace/tmp/1224.xlsx")
  return mergeData

def TestB():
  df1 = util.LoadData('stock_hold', 'dv1', condition={'diff': {'$lt': 0.1}}, sort=[('diff', 1)])
  df2 = util.LoadData('stock_statistcs', 'dvYears', condition={}, sort=[('百分比', -1)])
  
  mergeData = df1.join(df2, how='left', rsuffix='right')
  codes = []
  for code, row in mergeData.iterrows():
    codes.append(code)
  df3 = util.LoadData2('stock_backtest', 'all_dv1', codes)
  df4 = util.LoadData2('stock_statistcs', 'quarterSpeed', codes)
  df5 = util.LoadData2('stock', 'stock_list', codes)
  df6 = util.LastPriceNone(codes)
  df5 = df5[['所属行业', '地区', '总股本(亿)']]
  mergeData = mergeData.join(df3, how='left', rsuffix='right2')
  mergeData = mergeData.join(df4, how='left', rsuffix='right3')
  mergeData = mergeData.join(df5, how='left', rsuffix='right4')
  mergeData = mergeData.join(df6, how='left', rsuffix='right5')
  mergeData['markValue'] = mergeData['price'] * mergeData['总股本(亿)']
  mergeData.query('first > 0 and second > 0 and third > 0', inplace=True)
  mergeData.query('markValue >= 50', inplace=True)
  mergeData = mergeData[['name', 'diff', 'percent', '统计年数', '分红年数', 'maxValue:value', '所属行业', '地区', 'markValue']]
  
  # mergeData.eval('总市值 = price * 总股本(亿)', inplace=True)
  mergeData.to_excel("c:/workspace/tmp/1222-3.xlsx")
  return mergeData

  
if __name__ == '__main__':
  import strategy.dv1
  CODE_AND_MONEY = [
    # # # 皖通高速
    #   {'code': '600012', 'money': 52105},
    # # # 万华化学
    #   {'code': '600309', 'money': 146005},
    # # # 北京银行
    #   {'code': '601169', 'money': 88305},
    # # # 大秦铁路
    # # # 2015年4月27日那天，预警价为14.33元，但收盘价只有14.32元，我们按照收盘价计算，
    # # # 差一分钱才触发卖出规则。如果当时卖出，可收回现金14.32*12500+330=179330元。
    # # # 错过这次卖出机会后不久，牛市见顶，股价狂泻，从14元多一直跌到5.98元。
    # # # TODO 需要牛市清盘卖出策略辅助
    #   {'code': '601006', 'money': 84305},
    #南京银行
    # {'code': '601009', 'money': 75005},
    # 东风股份
    # {'code': '601515', 'money': 133705},
    # 福耀玻璃
    # {'code': '600660', 'money': 125905},
    # 光大银行
    # {'code': '601818', 'money': 29105},
    # 浦发银行
    # {'code': '600000', 'money': 74505},
    # 重庆水务
    # {'code': '601158', 'money': 58105},
    # 中国建筑
    # {'code': '601668', 'money': 29605},
    # 永新股份
    # {'code': '002014', 'money': 124305},
    # 万科
    # {'code': '000002', 'money': 72705},
    # 华域汽车
    # {'code': '600741', 'money': 92005},
    # 宇通客车
   # 再看历史PB情况，在2016年4月，宇通客车的PB位于3.84，中位值3.96，很显然，
    # 不具有很强的估值吸引力。也就是说，如果考虑估值因素，我们将不会买入。
    # TODO 买点看pb？
    # {'code': '600066', 'money': 203305},
    # 宝钢股份
    # TODO 买点看pb？
    # {'code': '600019', 'money': 70705},
    # 荣盛发展
    # {'code': '002146', 'money': 99205},
    # 厦门空港
    # {'code': '600897', 'money': 242805},
    # 金地集团
    # {'code': '600383', 'money': 103205},
    # 海螺水泥
    # {'code': '600585', 'money': 295905},
    # 长江电力
    # {'code': '600900', 'money': 63905},
    # 承德露露
    #可以看到，虽然承德露露目前属于高息股票，但从2011到2016年，它的分红一直不达标
    #TODO 需要持续分红剔除没有做到持续分红的标的
    # {'code': '000848', 'money': 97405},
    # 联发股份
    #TODO 这是一个股息率算法的典型例子，因为它每年分红两次（中报、年报），且常有送转股
    #缺少db.getCollection('gpfh-2015-12-31').find({"_id" : "002394"}) 数据
    # {'code': '002394', 'money': 149005},
    # 粤高速A
    # {'code': '000429', 'money': 75105},
    # 招商银行
    # {'code': '600036', 'money': 101505},
    # 鲁泰A
    # {'code': '000726', 'money': 93505},
  ]
  

  VERIFY_CODES = [
    # # # 皖通高速
    {'name': '皖通高速', '_id': '600012', 'money': 52105},
    # # # 万华化学
    {'name': '万华化学', '_id': '600309', 'money': 146005},
    # # # 北京银行
    {'name': '北京银行', '_id': '601169', 'money': 88305},
    # # # 大秦铁路
    # # # 2015年4月27日那天，预警价为14.33元，但收盘价只有14.32元，我们按照收盘价计算，
    # # # 差一分钱才触发卖出规则。如果当时卖出，可收回现金14.32*12500+330=179330元。
    # # # 错过这次卖出机会后不久，牛市见顶，股价狂泻，从14元多一直跌到5.98元。
    # # # TODO 需要牛市清盘卖出策略辅助
    {'name': '大秦铁路', '_id': '601006', 'money': 84305},
    # 南京银行
    {'name': '南京银行', '_id': '601009', 'money': 75005},
    # 东风股份
    {'name': '东风股份', '_id': '601515', 'money': 133705},
    # 福耀玻璃
     {'name': '福耀玻璃', '_id': '600660', 'money': 125905},
    # 光大银行
    {'name': '光大银行', '_id': '601818', 'money': 29105},
    # 浦发银行
    {'name': '浦发银行', '_id': '600000', 'money': 74505},
    # 重庆水务
    {'name': '重庆水务', '_id': '601158', 'money': 58105},
    # 中国建筑
    {'name': '中国建筑', '_id': '601668', 'money': 29605},
    # 永新股份
    {'name': '永新股份', '_id': '002014', 'money': 124305},
    # 万科
    {'name': '万科', '_id': '000002', 'money': 72705},
    # 华域汽车
    {'name': '华域汽车', '_id': '600741', 'money': 92005},
    # 宇通客车
    # 再看历史PB情况，在2016年4月，宇通客车的PB位于3.84，中位值3.96，很显然，
    # 不具有很强的估值吸引力。也就是说，如果考虑估值因素，我们将不会买入。
    # TODO 买点看pb？
    {'name': '宇通客车', '_id': '600066', 'money': 203305},
    # 宝钢股份
    # TODO 买点看pb？
    {'name': '宝钢股份', '_id': '600019', 'money': 70705},
    # 荣盛发展
    {'name': '荣盛发展', '_id': '002146', 'money': 99205},
    # 厦门空港
    {'name': '厦门空港', '_id': '600897', 'money': 242805},
    # 金地集团
    {'name': '金地集团', '_id': '600383', 'money': 103205},
    # 海螺水泥
    {'name': '海螺水泥', '_id': '600585', 'money': 295905},
    # 长江电力
    {'name': '长江电力', '_id': '600900', 'money': 63905},
    # 承德露露
    # 可以看到，虽然承德露露目前属于高息股票，但从2011到2016年，它的分红一直不达标
    # TODO 需要持续分红剔除没有做到持续分红的标的
    {'name': '承德露露', '_id': '000848', 'money': 97405},
    # 粤高速A
    {'name': '粤高速A', '_id': '000429', 'money': 75105},
    # 招商银行
    {'name': '招商银行', '_id': '600036', 'money': 101505},
    # 鲁泰A
    {'name': '鲁泰A', '_id': '000726', 'money': 93505},
  
    {'name': '中国石化', '_id': '600028', 'money': 74405},
    {'name': '双汇发展', '_id': '000895', 'money': 211205},
    {'name': '伟星股份', '_id': '002003', 'money': 80805},
    {'name': '兴业银行', '_id': '601166', 'money': 90205},
    {'name': '交通银行', '_id': '601328', 'money': 46905},
    {'name': '方大特钢', '_id': '600507', 'money': 167905},
    #TODO 增加pb指标
    {'name': '中国神华', '_id': '601088', 'money': 219705},
    {'name': '新城控股', '_id': '601155', 'money': 102805},
    {'name': '农业银行', '_id': '601288', 'money': 26405},
    #2017年全年无分红，2018年出年报就该卖出
    {'name': '格力电器', '_id': '000651', 'money': 296305},

  ]
  #上证红利50
  BONUS_CODES = [
    {'name': "宝钢股份", '_id': "600019"}, {'name': "浙能电力", '_id': "600023"}, {'name': "中国石化", '_id': "600028"},
    {'name': "福建高速", '_id': "600033"}, {'name': "保利地产", '_id': "600048"}, {'name': "宇通客车", '_id': "600066"},
    {'name': "上汽集团", '_id': "600104"}, {'name': "东睦股份", '_id': "600114"}, {'name': "香江控股", '_id': "600162"},
    {'name': "雅戈尔", '_id': "600177"}, {'name': "赣粤高速", '_id': "600269"}, {'name': "南钢股份", '_id': "600282"},
    {'name': "华发股份", '_id': "600325"}, {'name': "山东高速", '_id': "600350"}, {'name': "首开股份", '_id': "600376"},
    {'name': "宁沪高速", '_id': "600377"}, {'name': "金地集团", '_id': "600383"}, {'name': "海澜之家", '_id': "600398"},
    {'name': "方大特钢", '_id': "600507"}, {'name': "深高速", '_id': "600548"}, {'name': "迪马股份", '_id': "600565"},
    {'name': "海螺水泥", '_id': "600585"}, {'name': "申能股份", '_id': "600642"}, {'name': "福耀玻璃", '_id': "600660"},
    {'name': "川投能源", '_id': "600674"}, {'name': "上海石化", '_id': "600688"}, {'name': "物产中大", '_id': "600704"},
    {'name': "华域汽车", '_id': "600741"}, {'name': "马钢股份", '_id': "600808"}, {'name': "梅花生物", '_id': "600873"},
    {'name': "厦门空港", '_id': "600897"}, {'name': "长江电力", '_id': "600900"}, {'name': "恒源煤电", '_id': "600971"},
    {'name': "柳钢股份", '_id': "601003"}, {'name': "大秦铁路", '_id': "601006"}, {'name': "南京银行", '_id': "601009"},
    {'name': "中国神华", '_id': "601088"}, {'name': "兴业银行", '_id': "601166"}, {'name': "农业银行", '_id': "601288"},
    {'name': "交通银行", '_id': "601328"}, {'name': "工商银行", '_id': "601398"},{'name': "九牧王", '_id': "601566"},
    {'name': "旗滨集团", '_id': "601636"}, {'name': "光大银行", '_id': "601818"}, {'name': "建设银行", '_id': "601939"},
    {'name': "中国银行", '_id': "601988"}, {'name': "中信银行", '_id': "601998"}, {'name': "养元饮品", '_id': "603156"},
    {'name': "渤海轮渡", '_id': "603167"}, {'name': "依顿电子", '_id': "603328"},
    ]
  # for one in VERIFY_CODES:
  #   stock = TradeUnit(one['_id'], one['money'])
  #   if not stock.ExistCheckResult():
  #     print(stock.code)
  # TestBank()
  # SignalAll()
  # CalcDVAll()
  
  # HoldAll()
  # df1 = TestA()
  # df2 = TestB()
  # merge = pd.merge(df1, df2)
  # merge2 =df1.join(df2, how='inner', rsuffix='right')
  # merge = merge[['name', 'diff', 'percent', '统计年数', '分红年数', 'maxValue:value', '所属行业', '地区', 'markValue']]
  # merge.to_excel("c:/workspace/tmp/1223-merge.xlsx")
  # print(merge)
  # print(merge2)
  # strategy.dv1.SignalDV([{'_id': '600900', 'name': '长江电力'}])

  # client = MongoClient()
  # db = client["stock_backtest"]
  # collection = db["all_dv1"]
  # cursor = collection.find({'tradeCounter': {'$gt': 0}})
  # out = []
  # for c in cursor:
  #   out.append(c)
  #
  # strategy.dv1.CalcQuarterSpeed(out, 2019)
  
  
  # strategy.dv1.CalcDV([{'_id': '002085', 'name': ''}, {'_id': '002191', 'name': ''}])
  # TestTwo(
  #         # [
  #         #   {'_id': '600025', 'name': '华能水电', },
  #         #   {'_id': '601166', 'name': '兴业银行', 'money': 90205},
  #         #   {'_id': '600900', 'name': '长江电力', 'money': 63905},
  #         #  ],
  #   [
  #     {'_id': '603118', 'name': '共进股份', },
  #   ],
  #   100000, {'saveprepare': 1, 'backtest':1})
  # test
  # TestAll(CODE_AND_MONEY, True, False)
  #save
  TestTwo(VERIFY_CODES, 100000, {'check': 1, 'backtest': 1})
  # TestAll(VERIFY_CODES, True, False)
  #check
  # TestAll(VERIFY_CODES, False, True)
  #compare
  # CompareAll(VERIFY_CODES)

  
  # strategy.dv1.Digest('all_dv1',   {"$where": "this.percent > this.hs300Profit"})
  #TODO 周末研究下怎么画图，把入出点放在图形上，更直观，hs300，股价，收益曲线