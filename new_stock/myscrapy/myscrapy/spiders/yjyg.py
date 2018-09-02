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

def String2Number(s):
  out = np.nan
  try:
    out = float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])
  except Exception as e:
    pass

  return out


def todayString():
  now = datetime.datetime.now()
  now = now.replace(hour=0, minute=0, second=0, microsecond=0)
  return now.strftime('%Y-%m-%d')


class Spider(scrapy.Spider):
  name = 'stock-yjyg'
  startYear = 2017
  baseURL = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?'

  MONGODB_ID = const.MONGODB_ID
  ID_NAME = const.YJYG_KEYWORD.ID_NAME
  DB_NAME = const.YJYG_KEYWORD.DB_NAME
  COLLECTION_HEAD = const.YJYG_KEYWORD.COLLECTION_HEAD
  KEY_NAME = const.YJYG_KEYWORD.KEY_NAME
  NEED_TO_NUMBER = const.YJYG_KEYWORD.NEED_TO_NUMBER
  DATA_SUB = const.YJYG_KEYWORD.DATA_SUB

  allowed_domains = [
    'data.eastmoney.com',
    'dcfm.eastmoney.com',
  ]
  start_urls = [
    'http://data.eastmoney.com/bbsj/201806/yjyg.html'
  ]

  headers = {
    'Host': 'data.eastmoney.com',
    'Referer': 'http://data.eastmoney.com/yjfp/201712.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
  }

  xpath = {
    # 'quarterList': '/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/select/option',
    'quarterList': '/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/select',

  }

  received = set()


  def genParams(self, page, date):
    params = {
      'type': 'YJBB20_YJYG',
      'token': '70f12f2f4f091e459a279469fe49eca5',
      'st': 'ndate',
      'sr': '-1',
      'p': page,
      'ps': '30',
      'js': 'var aUDOBatW={pages:(tp),data: (x)}',
      'filter': '(IsLatest=\'T\')(enddate=^' + date + '^)',
      'rt': int(time.time()),
    }
    return params

  def parseQuarter(self, response):

    re = []
    pq = pyquery.PyQuery(response.body)
    dataList = pq('#date_type')
    out = dataList.find('option')
    for one in out:
      year = float(one.text[:4])
      if year > self.startYear:
        re.append((self.baseURL + encode_params(self.genParams(1, one.text)), one.text))

    # ones = response.xpath(self.xpath['quarterList'])
    # for one in ones:
    #   text = one.xpath('./text()').extract().strip()
    #   year = float(text[:4])
    #   if year > self.startYear:
    #     re.append(self.baseURL + encode_params(self.genParams(1, text)))

    return re


  def nextPage(self, json, meta):
    out = []
    if 'pages' in json:
      total = json.get('pages')
      for i in range(2, total + 1):
        out.append(self.baseURL + encode_params(self.genParams(i, meta['quarter'])))

    return out



  def parsePage(self, json):
    try:
      tmp = []
      for item in json:
        one_stock = util.utils.dealwithData(item, util.utils.threeOP(self.DATA_SUB,
                                                                     self.NEED_TO_NUMBER, self.KEY_NAME))
        one_stock[self.MONGODB_ID] = item.get(self.ID_NAME)
        series = pd.Series(one_stock)
        tmp.append(series)

      df = pd.DataFrame(tmp)
      print(df)
      return df
    except Exception as e:
      logging.warning("parsePage Exception %s" % (str(e)))

  def saveDB(self, data: pd.DataFrame, date):

    re = util.saveMongoDB(data, util.genEmptyFunc(), self.DB_NAME, self.COLLECTION_HEAD + date, None)
    util.everydayChange(re, 'yjyg')

  def parse(self, response):
    self.received.add(response.url)

    if 'step' not in response.meta:
      quarter = self.parseQuarter(response)
      # realOut = set(quarter) - self.received
      for one in quarter:
        yield Request(one[0], meta={'step': 1, 'quarter': one[1]})


    if 'step' in response.meta:
      json_data = {}
      if response.meta['step'] >= 1:
        content = response.body[13:]
        try:
          data = content.decode('utf-8')
          data = data.replace('pages', '"pages"', 1)
          data = data.replace('data', '"data"', 1)
          json_data = json.loads(data)
        except Exception as e:
          logging.warning("parse json Exception %s" % (str(e)))

        if response.meta['step'] == 1:
          nextPage = self.nextPage(json_data, response.meta)
          # realOut = set(nextPage) - self.received
          for one in nextPage:
            yield Request(one, meta={'step': 2, 'quarter': response.meta['quarter']})

        if 'data' in json_data:
          data = json_data.get('data')
          df = self.parsePage(data)
          if len(df):
            self.saveDB(df, response.meta['quarter'])


