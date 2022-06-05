#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-30 05:28:16
# Project: yjyg_2018


# sys
import json
import time
# thirdpart
import pandas as pd
import numpy as np
from requests.models import RequestEncodingMixin
encode_params = RequestEncodingMixin._encode_params
#from HTMLParser import HTMLParser

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const
from fake_spider import spider
try:
  import setting
except Exception as e:
  print(e)

MONGODB_ID = const.MONGODB_ID
ID_NAME = const.YJBG2_KEYWORD.ID_NAME
DB_NAME = const.YJBG2_KEYWORD.DB_NAME
COLLECTION_HEAD = const.YJBG2_KEYWORD.COLLECTION_HEAD
KEY_NAME = const.YJBG2_KEYWORD.KEY_NAME
NONE_TO_NUMBER = const.YJBG2_KEYWORD.NONE_TO_NUMBER
DATA_SUB = const.YJBG2_KEYWORD.DATA_SUB
# STOCK_LIST = setting.f_data_stocklist()
# STOCK_LIST = ['000636']



base_url = 'https://datacenter-web.eastmoney.com/api/data/v1/get?'




class Handler(spider.FakeSpider):
  crawl_config = {
  }
  STOCK_LIST = None
  def on_start(self):
    out = self.url()
    for one in out:
      save = {'key': one[1]}
      self.crawl(one[0], headers=self.header(), callback=self.processFirstPage, save=save)

  def genParams(self, code):
    """
    https://datacenter-web.eastmoney.com/api/data/v1/get?
    callback=jQuery112307970225087254572_1654332516847
    &sortColumns=REPORTDATE
    &sortTypes=-1
    &pageSize=50
    &pageNumber=1
    &columns=ALL
    &filter=(SECURITY_CODE="000636")
    &reportName=RPT_LICO_FN_CPD
    """
    params = {
      'callback': 'Query112307970225087254572_1654332516847',
      'sortColumns': 'REPORTDATE',
      'pageSize': '50',
      # 虽然可能存在p多于1页的情况，但是目前先不考虑这种情况
      'pageNumber': '1',
      'columns': 'ALL',
      'filter': '(SECURITY_CODE="' + code + '")',
      'reportName': "RPT_LICO_FN_CPD"
    }
    return params



  def url(self):
    out = []
    STOCK_LIST = None
    if Handler.STOCK_LIST is not None:
      STOCK_LIST = Handler.STOCK_LIST
    else:
      STOCK_LIST = setting.f_data_stocklist()
    for code in STOCK_LIST:
      url = encode_params(self.genParams(code))
      url = base_url + url
      out.append((url, code))

    return out


  def header(self):
    headers = {
      'Host': 'datacenter-web.eastmoney.com',
      'Referer': 'https://data.eastmoney.com/',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
    }
    return headers


  def saveDB(self, data: pd.DataFrame, key):
    tableName = "{}{}".format(COLLECTION_HEAD, key)
    print("tableName: {}".format(tableName))
    def callback(result):
      self.send_message(self.project_name, result, key + '_' + result[MONGODB_ID])

    util.saveMongoDB(data, util.genEmptyFunc(), DB_NAME, tableName, callback)


  def processFirstPage(self, response):
    if response.ok == False:
      return

    content = response.content[13:]
    print(response.url)
    save = response.save
    code = save['key']
    try:
      data = content.decode('utf-8')
      print(data)
      index = data.find("(")
      realData = data[index+1:-2]

      json_data = json.loads(realData)  # , encoding='GB2312')
      results = self.processDetailPage(json_data, code)
      self.saveDB(results, code)
    except UnicodeDecodeError as e:
      print(e)
    except Exception as e:
      print(e)



  def processDetailPage(self, json, code):
    if json:

      data = json.get('result')['data']
      return self.parse_page(data)



  def parse_page(self, data):
    """
    {"SECURITY_CODE":"601939",
    "SECURITY_NAME_ABBR":"建设银行",
    "TRADE_MARKET_CODE":"069001001001",
    "TRADE_MARKET":"上交所主板",
    "SECURITY_TYPE_CODE":"058001001",
    "SECURITY_TYPE":"A股",
    "UPDATE_DATE":"2022-04-30 00:00:00",
    "REPORTDATE":"2022-03-31 00:00:00",
    "BASIC_EPS":0.35,
    "DEDUCT_BASIC_EPS":null,
    "TOTAL_OPERATE_INCOME":232230000000,
    "PARENT_NETPROFIT":88741000000,
    "WEIGHTAVG_ROE":3.505,
    "YSTZ":7.2541947045,
    "SJLTZ":6.77,
    "BPS":10.292767118247,
    "MGJYXJJE":1.919675534276,
    "XSMLL":null,
    "YSHZ":16.2074,
    "SJLHZ":26.1242,
    "ASSIGNDSCRPT":null,
    "PAYYEAR":null,
    "PUBLISHNAME":"银行",
    "ZXGXL":null,
    "NOTICE_DATE":"2022-04-30 00:00:00",
    "ORG_CODE":"10008225",
    "TRADE_MARKET_ZJG":"0101",
    "ISNEW":"1",
    "QDATE":"2022Q1",
    "DATATYPE":"2022年 一季报",
    "DATAYEAR":"2022",
    "DATEMMDD":"一季报",
    "EITIME":"2022-04-29 20:33:03",
    "SECUCODE":"601939.SH"},
    """
    try:
      tmp = []
      for item in data:
        # item['roeweighted'] = util.utils.yjyg_unescape(mapping, item['roeweighted'])
        # item['totaloperatereve'] = util.utils.yjyg_unescape(mapping, item['totaloperatereve'])
        # item['xsmll'] = util.utils.yjyg_unescape(mapping, item['xsmll'])
        # item['parentnetprofit'] = util.utils.yjyg_unescape(mapping, item['parentnetprofit'])
        #
        # #以下字段目前未使用
        # item['basiceps'] = util.utils.yjyg_unescape(mapping, item['basiceps'])
        # item['cutbasiceps'] = util.utils.yjyg_unescape(mapping, item['cutbasiceps'])
        # item['ystz'] = util.utils.yjyg_unescape(mapping, item['ystz'])
        # item['yshz'] = util.utils.yjyg_unescape(mapping, item['yshz'])
        # item['sjltz'] = util.utils.yjyg_unescape(mapping, item['sjltz'])
        # item['sjlhz'] = util.utils.yjyg_unescape(mapping, item['sjlhz'])
        # item['bps'] = util.utils.yjyg_unescape(mapping, item['bps'])
        # item['mgjyxjje'] = util.utils.yjyg_unescape(mapping, item['mgjyxjje'])
        # item['assigndscrpt'] = util.utils.yjyg_unescape(mapping, item['assigndscrpt'])
        # item['gxl'] = util.utils.yjyg_unescape(mapping, item['gxl'])

        newItem = {}
        newItem['reportdate'] = item['REPORTDATE']
        newItem['basiceps'] = item['BASIC_EPS']
        newItem['cutbasiceps'] = item['DEDUCT_BASIC_EPS']
        newItem['totaloperatereve'] = item['TOTAL_OPERATE_INCOME']
        newItem['ystz'] = item['YSTZ']
        newItem['yshz'] = item['YSHZ']
        newItem['parentnetprofit'] = item['PARENT_NETPROFIT']
        newItem['sjltz'] = item['SJLTZ']
        newItem['sjlhz'] = item['SJLHZ']
        newItem['bps'] = item['BPS']
        newItem['roeweighted'] = item['WEIGHTAVG_ROE']
        newItem['mgjyxjje'] = item['MGJYXJJE']
        newItem['xsmll'] = item['XSMLL']
        newItem['assigndscrpt'] = item['ASSIGNDSCRPT']
        newItem['gxl'] = item['ZXGXL']
        newItem['firstnoticedate'] = item['NOTICE_DATE']
        newItem['latestnoticedate'] = item['UPDATE_DATE']



        one_stock = util.utils.dealwithData(newItem, util.utils.threeOP(DATA_SUB,
                                                                     NONE_TO_NUMBER, KEY_NAME))

        one_stock[MONGODB_ID] = one_stock[ID_NAME]

        #下面两个都是百分数
        if isinstance(one_stock[KEY_NAME['roeweighted']], float):
          one_stock[KEY_NAME['roeweighted']] /= 100
        if isinstance(one_stock[KEY_NAME['xsmll']], float):
          one_stock[KEY_NAME['xsmll']] /= 100
        #计算销售净利率
        if isinstance(one_stock[KEY_NAME['parentnetprofit']], float) and isinstance(one_stock[KEY_NAME['totaloperatereve']], float):
          try:
            one_stock[KEY_NAME['xsjll']] = one_stock[KEY_NAME['parentnetprofit']] / one_stock[KEY_NAME['totaloperatereve']]
          except:
            one_stock[KEY_NAME['xsjll']] = np.nan

        series = pd.Series(one_stock)
        tmp.append(series)

      df = pd.DataFrame(tmp)
      print(df)
      return df
    except Exception as e:
      print(e)


  def on_message(self, project, msg):
    return msg


def run():
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()


def TestRun():
  Handler.STOCK_LIST = ['601398', '000002']
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()


if __name__ == '__main__':
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()
