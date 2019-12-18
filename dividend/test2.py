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
import strategy.dv1



if __name__ == '__main__':
  # 沪深300计算#############################################
  df = util.QueryHS300All()
  out = []
  # for code, row in df.iterrows():
  #   stock = strategy.dv1.TradeUnit(code, row['股票名称'], 100000)
  #   stock.collectionName = 'hs300_dv1'
  #   stock.LoadQuotations()
  #   stock.LoadIndexs()
  #   stock.Merge()
  #   stock.CheckPrepare()
  #
  #   print(stock.checkPoint)
  #   print(stock.dangerousPoint)
  #   for one in stock.dividendPoint:
  #     print(one)
  #
  #   stock.BackTest()
  #   stock.CloseAccount()
  #   stock.Store2DB()

  #沪深300统计##############################################
  df = util.QueryHS300All()
  out = []
  for code, row in df.iterrows():
    out.append({'code': code, 'name': row['股票名称']})

  strategy.dv1.CompareAll('hs300_dv1', out)

  #全部股票################################################
  # df = util.QueryAll()
  # out = []
  # client = MongoClient()
  # db = client['stock_backtest']
  # collection = db['all_dv1']
  # cursor = collection.find()
  # already = set()
  # for c in cursor:
  #   already.add(c['_id'])
  #
  # for code, row in df.iterrows():
  #   if code in already:
  #     continue
  #   stock = strategy.dv1.TradeUnit(code, row['名称'], 100000)
  #   stock.collectionName = 'all_dv1'
  #   stock.LoadQuotations()
  #   stock.LoadIndexs()
  #   stock.Merge()
  #   stock.CheckPrepare()
  #
  #   print(stock.checkPoint)
  #   print(stock.dangerousPoint)
  #   for one in stock.dividendPoint:
  #     print(one)
  #
  #   stock.BackTest()
  #   stock.CloseAccount()
  #   stock.Store2DB()

  # df = util.QueryAll()
  # out = []
  # for code, row in df.iterrows():
  #   out.append({'code': code, 'name': row['名称']})
  #
  # strategy.dv1.CompareAll('all_dv1', out)