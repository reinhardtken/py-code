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

  # use it to create stockList and hs300 when the first time and mongodb is empty
  import fake_spider.tushare.hs300
  # fake_spider.tushare.hs300.saveDB(fake_spider.tushare.hs300.getHS300())
  # import fake_spider.tushare.stockList
  # fake_spider.tushare.stockList.saveDB(fake_spider.tushare.stockList.getBasics())

  # fake_spider.tushare.kData.RunHS300Index()
  # codes = queryAllCode()

  # k线数据
  # for code in codes:
  #   try:
  #     print('process {} ############################################'.format(code))
  #     fake_spider.tushare.kData.RunOneNone(code)
  #   except Exception as e:
  #     print(e)
  fake_spider.tushare.kData.RunOneNone('001872')
  fake_spider.tushare.kData.RunOneNone('601298')
  # #拿季报增速
  # try:
  #   fake_spider.yjbg.Handler.STOCK_LIST = codes
  #   fake_spider.yjbg.run()
  # except Exception as e:
  #   print(e)
  #
  # #拿年报分红
  # try:
  #   fake_spider.gpfh.Handler.ALL = True
  #   fake_spider.gpfh.run()
  # except Exception as e:
  #   print(e)



