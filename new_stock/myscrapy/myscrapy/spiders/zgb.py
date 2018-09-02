# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime
import time
import json
import random

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
import const.TS as TS
import query.query_hs300 as query


class Spider(scrapy.Spider):
  name = 'stock-zgb'
  # startYear = 2017
  # baseURL = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?'

  MONGODB_ID = const.MONGODB_ID
  DB_NAME = TS.BASICS.DB_NAME
  COLLECTION_NAME = TS.BASICS.COLLECTION_NAME

  jsonCallBack = 'jsonpCallback24417'

  allowed_domains = [
    'www.szse.cn',
    'query.sse.com.cn',
  ]
  start_urls = [
    'http://www.szse.cn'
  ]

  headers = {
    # 'Host': 'data.eastmoney.com',
    # 'Referer': 'http://data.eastmoney.com/yjfp/201712.html',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
  }

  xpath = {
  }

  received = set()


  def szBaseURL(self):
    return 'http://www.szse.cn/api/report/index/companyGeneralization?'

  def shBaseURL(self):
    return 'http://query.sse.com.cn/security/stock/queryCompanyStockStruct.do?'

  def genSZParams(self, code):
    params = {
      'random': random.random(),
      'secCode': code,# = 000725
    }
    return params

  def genSHParams(self, code):
    params = {
      'jsonCallBack': self.jsonCallBack,
      'isPagination': 'false',
      'companyCode': code,
      '_': int(time.time()),
    }
    return params


  @property
  def stock_list(self):
    out = []
    out.extend(query.queryCodeList())
    out.extend(const.STOCK_LIST)
    return out

  def genStockList(self):
    out = []
    for code in self.stock_list:
      base = self.shBaseURL() if code.startswith('6') else self.szBaseURL()
      params = self.genSHParams(code) if code.startswith('6') else self.genSZParams(code)
      url = encode_params(params)
      url = base + url
      if code.startswith('6'):
        out.append((url, code, self.shHeader(code)))
      else:
        out.append((url, code, self.szHeader(code)))

    return out


  def szHeader(self, code):
    headers = {
      'Host': 'www.szse.cn',
      'Referer': 'http://www.szse.cn/certificate/individual/index.html?code=' + code,
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
      'X-Request-Type': 'ajax',
      'X-Requested-With': 'XMLHttpRequest',
    }
    return headers

  def shHeader(self, code):
    headers = {
      'Host': 'query.sse.com.cn',
      'Referer': 'http://www.sse.com.cn/assortment/stock/list/info/capital/index.shtml?COMPANY_CODE=' + code,
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
      #'X-Request-Type': 'ajax',
      #'X-Requested-With': 'XMLHttpRequest',
    }
    return headers



  def parsePage(self, code, data):
    if code.startswith('6'):
      data = data[len(self.jsonCallBack) + 1:-1]
      json_data = json.loads(data)
      result = self.parseSHPage([json_data['result'], ])
      self.saveDB(result, code)
      pass
    else:
      json_data = json.loads(data)
      if json_data['code'] == '0':
        result = self.parseSZPage([json_data['data'], ])
        self.saveDB(result, code)

  def parseSZPage(self, json):
    KEY_NAME = {
      'agzgb': 'A股总股本',
      'bgzgb': 'B股总股本',
      'zgb': TS.BASICS.KEY_NAME['zgb'],
    }
    NEED_TO_NUMBER = {
      'agzgb': 'A股总股本',
      'bgzgb': 'B股总股本',
    }
    NOTEAT = {
      'agzgb': None,
      'bgzgb': None,
    }
    DATA_SUB = {}
    try:
      tmp = []
      for item in json:
        one_stock = util.utils.dealwithData(item, util.utils.fourOP(DATA_SUB, NEED_TO_NUMBER,
                                                                    NOTEAT, KEY_NAME))

        one_stock[KEY_NAME['agzgb']] = one_stock[KEY_NAME['agzgb']] * 10000
        one_stock[KEY_NAME['bgzgb']] = one_stock[KEY_NAME['bgzgb']] * 10000
        re = {}
        re[KEY_NAME['zgb']] = one_stock[KEY_NAME['bgzgb']] + one_stock[KEY_NAME['agzgb']]
        series = pd.Series(re)
        tmp.append(series)

      df = pd.DataFrame(tmp)
      print(df)
      return df
    except Exception as e:
      print(e)

  def parseSHPage(self, json):
    KEY_NAME = {
      'totalShares': '总股本',
      'zgb': TS.BASICS.KEY_NAME['zgb'],
    }
    NEED_TO_NUMBER = {
      'totalShares': '总股本',
    }
    NOTEAT = {
      'totalShares': None,
    }
    DATA_SUB = {}
    try:
      tmp = []
      for item in json:
        one_stock = util.utils.dealwithData(item, util.utils.fourOP(DATA_SUB, NEED_TO_NUMBER,
                                                                    NOTEAT, KEY_NAME))
        re = {}
        re[KEY_NAME['zgb']] = one_stock[KEY_NAME['totalShares']] * 10000
        series = pd.Series(re)
        tmp.append(series)

      df = pd.DataFrame(tmp)
      print(df)
      return df
    except Exception as e:
      print(e)

  def saveDB(self, data: pd.DataFrame, code):
    util.updateMongoDB(data, util.genKeyIDFunc(code), self.DB_NAME, self.COLLECTION_NAME, False, None)


  def parse(self, response):
    self.received.add(response.url)

    if 'step' not in response.meta:
      code = self.genStockList()
      # realOut = set(quarter) - self.received
      for one in code:
        yield Request(one[0], meta={'step': 1, 'code': one[1]}, headers=one[2])


    if 'step' in response.meta:
      json_data = {}
      if response.meta['step'] >= 1:

        content = response.body
        try:
          data = content.decode('utf-8')
          # json_data = json.loads(data)
        except Exception as e:
          logging.warning("parse json Exception %s" % (str(e)))

        self.parsePage(response.meta['code'], data)
        # if len(df):
        #   self.saveDB(df, response.meta['code'])


