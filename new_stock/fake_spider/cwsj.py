#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-28 04:28:42
# Project: gpfh


# sys
import json
# thirdpart
import pandas as pd
from requests.models import RequestEncodingMixin

encode_params = RequestEncodingMixin._encode_params

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const
from fake_spider import spider

base_url = 'http://emweb.securities.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?'


class Handler(spider.FakeSpider):
  crawl_config = {
  }

  def on_start(self):
    out = self.url()
    for one in out:
      save = {'key': one[1]}
      self.crawl(one[0], headers=self.header(), callback=self.processFirstPage, save=save)

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

  def url(self):

    out = []
    for code in const.STOCK_LIST:
      url = encode_params(self.genParams(code))
      url = base_url + url
      out.append((url, code))

    return out

  def header(self):
    headers = {
      'Host': 'emweb.securities.eastmoney.com',
      'Referer': 'http://emweb.securities.eastmoney.com/NewFinanceAnalysis/Index?type=web&code=SZ000725',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
      'X-Requested-With': 'XMLHttpRequest',
    }
    return headers

  def saveDB(self, data: pd.DataFrame, key):
    def callback(result):
      self.send_message(self.project_name, result, key + '_' + result['_id'])

    util.saveMongoDB(data, util.genEmptyFunc(), 'stock', 'cwsj-' + key, callback)

  def processFirstPage(self, response):
    if response.ok == False:
      return

    data = response.content.decode('utf-8')
    json_data = json.loads(data)
    result = self.parse_page(json_data)
    save = response.save
    self.saveDB(result, save['key'])

  def parse_page(self, json):
    try:
      tmp = []
      for item in json:
        one_stock = util.utils.dealwithData(item, util.utils.threeOP(const.CWSJ_KEYWORD.KEY_NAME, {},
                                                                     const.CWSJ_KEYWORD.NEED_TO_NUMBER))
        one_stock['_id'] = item.get('date')
        series = pd.Series(one_stock)
        tmp.append(series)

      df = pd.DataFrame(tmp)
      print(df)
      return df
    except Exception as e:
      print(e)

  def on_message(self, project, msg):
    return msg


def readList():
  import xlrd

  workbook = xlrd.open_workbook('/home/ken/workspace/tmp/in.xlsx')

  sheet = workbook.sheet_by_name('股票池')
  '''
  sheet.nrows　　　　sheet的行数
  sheet.row_values(index)　　　　返回某一行的值列表
　　sheet.row(index)　　　　返回一个row对象，可以通过row[index]来获取这行里的单元格cell对象'''
  nrows = sheet.nrows
  out = []
  for index in range(1, nrows):
    print(nrows)
    row = sheet.row(index)
    out.append(row[0].value)

  for one in out:
    print('"' + str(one) + '",')


if __name__ == '__main__':
  # readList()
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()
