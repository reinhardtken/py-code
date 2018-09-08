# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime
import time
import json

import pyquery
import scrapy
from scrapy.http import Request
from scrapy.http import Response
import pandas as pd
import numpy as np
from requests.models import RequestEncodingMixin
encode_params = RequestEncodingMixin._encode_params

import items
import util
import util.utils
import const
import setting
# import query.query_hs300

class Spider(scrapy.Spider):
  name = 'stock-cwsj'
  startYear = 2017
  baseURL = 'http://emweb.securities.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?'

  MONGODB_ID = const.MONGODB_ID
  ID_NAME = const.CWSJ_KEYWORD.ID_NAME
  DB_NAME = const.CWSJ_KEYWORD.DB_NAME
  COLLECTION_HEAD = const.CWSJ_KEYWORD.COLLECTION_HEAD
  KEY_NAME = const.CWSJ_KEYWORD.KEY_NAME
  NEED_TO_NUMBER = const.CWSJ_KEYWORD.NEED_TO_NUMBER
  DATA_SUB = const.CWSJ_KEYWORD.DATA_SUB
  # STOCK_LIST = const.STOCK_LIST
  # STOCK_LIST = {'600028'}
  # STOCK_LIST = {'000725'}
  STOCK_LIST = setting.currentStockList()
  # KEY = 'var XbnsgnRv'

  allowed_domains = [
    'www.eastmoney.com',
    'emweb.securities.eastmoney.com',
  ]
  start_urls = [
    'http://www.eastmoney.com'
  ]

  headers = {
    'Host': 'emweb.securities.eastmoney.com',
    'Referer': 'http://emweb.securities.eastmoney.com/NewFinanceAnalysis/Index?type=web&code=SZ000725',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
  }

  xpath = {
  }

  received = set()

  def genParams(self, code):
    def addHead(code):
      if code.startswith('6'):
        return 'SH' + code
      elif code.startswith('0') or code.startswith('3'):
        return 'SZ' + code

    code = addHead(code)
    params = {
      'ctype': 4,
      'type': 0,
      'code': code,  # = SZ000725

    }
    return params

  def genStockList(self):
    out = []
    for code in self.STOCK_LIST:
      url = encode_params(self.genParams(code))
      url = self.baseURL + url
      out.append((url, code))

    return out



  def parsePage(self, json):
    try:
      tmp = []
      for item in json:
        one_stock = util.utils.dealwithData(item, util.utils.threeOP(self.DATA_SUB, self.NEED_TO_NUMBER, self.KEY_NAME))
        one_stock[self.MONGODB_ID] = item.get(self.ID_NAME)
        series = pd.Series(one_stock)
        tmp.append(series)

      df = pd.DataFrame(tmp)
      return df
    except Exception as e:
      logging.warning("parsePage Exception %s" % (str(e)))

  def saveDB(self, data: pd.DataFrame, date):

    re = util.saveMongoDB(data, util.genEmptyFunc(), self.DB_NAME, self.COLLECTION_HEAD + date, None)
    util.everydayChange(re, 'cwsj')

  def parse(self, response):
    self.received.add(response.url)

    if 'step' not in response.meta:
      code = self.genStockList()
      # realOut = set(quarter) - self.received
      for one in code:
        yield Request(one[0], meta={'step': 1, 'code': one[1]})


    if 'step' in response.meta:
      json_data = {}
      if response.meta['step'] >= 1:

        content = response.body
        try:
          data = content.decode('utf-8')
          json_data = json.loads(data)
        except Exception as e:
          logging.warning("parse json Exception %s" % (str(e)))

        # if response.meta['step'] == 1:
          # nextPage = self.nextPage(json_data, response.meta)
          # # realOut = set(nextPage) - self.received
          # for one in nextPage:
          #   yield Request(one, meta={'step': 2, 'quarter': response.meta['quarter']})

        df = self.parsePage(json_data)
        if len(df):
          self.saveDB(df, response.meta['code'])



