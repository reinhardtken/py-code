#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from pymongo import MongoClient





def queryAllCode():
  from pymongo import MongoClient
  client = MongoClient()
  db = client['stock']
  collection = db['stock_list']
  out = []
  cursor = collection.find()
  for c in cursor:
    out.append(c["_id"])
  
  return out


if __name__ == '__main__':
  import fake_spider.yjbg
  import fake_spider.gpfh
  import fake_spider.tushare.kData
  import fake_spider.tushare.hs300
  import fake_spider.tushare.stockList
  
  #获取沪深300标的的基本信息
  fake_spider.tushare.hs300.saveDB(fake_spider.tushare.hs300.getHS300())
  #获取全部股票的基本信息
  fake_spider.tushare.stockList.saveDB(fake_spider.tushare.stockList.getBasics())
  #获取沪深300的K线
  fake_spider.tushare.kData.RunHS300Index()
  #获取全部股票的不复权K线
  codes = queryAllCode()
  # k线数据
  for code in codes:
    try:
      print('process {} ############################################'.format(code))
      fake_spider.tushare.kData.RunOneNone(code)
    except Exception as e:
      print(e)

  #获取全部股票的季报增速
  try:
    fake_spider.yjbg.Handler.STOCK_LIST = codes
    fake_spider.yjbg.run()
  except Exception as e:
    print(e)
  
  #获取全部股票的年报分红
  try:
    fake_spider.gpfh.Handler.ALL = True
    fake_spider.gpfh.run()
  except Exception as e:
    print(e)



