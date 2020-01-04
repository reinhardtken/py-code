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
  # import fake_spider.yjyg
  # import fake_spider.tushare.kData
  # import fake_spider.tushare.hs300
  # import fake_spider.tushare.stockList
  # import fake_spider.cwsj
  # import fake_spider.gpfh
  # import fake_spider.m012
  # import fake_spider.zgb3
  # import adjust.cwsj_manager
  # import sys
  #
  # sys.path.append(r'C:\workspace\code\self\github\py-code\new_stock')
  # import fake_spider.tushare.kData
  # import fake_spider.yjbg
  # import fake_spider.marketvaluea
  # import myquery

  fake_spider.tushare.kData.RunHS300Index()
  codes = queryAllCode()
  for code in codes:
    try:
      print('process {} ############################################'.format(code))
      fake_spider.tushare.kData.RunOneNone(code)
    except Exception as e:
      print(e)
  



