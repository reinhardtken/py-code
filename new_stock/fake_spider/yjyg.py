#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-30 05:28:16
# Project: yjyg_2018


# sys
import json
import time
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

MONGODB_ID = const.MONGODB_ID
ID_NAME = const.YJYG_KEYWORD.ID_NAME
DB_NAME = const.YJYG_KEYWORD.DB_NAME
COLLECTION_HEAD = const.YJYG_KEYWORD.COLLECTION_HEAD
KEY_NAME = const.YJYG_KEYWORD.KEY_NAME
NEED_TO_NUMBER = const.YJYG_KEYWORD.NEED_TO_NUMBER
DATA_SUB = const.YJYG_KEYWORD.DATA_SUB


KEY = 'var XbnsgnRv'
'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?' \
'type=YJBB20_YJYG' \
'&token=70f12f2f4f091e459a279469fe49eca5' \
'&st=ndate&sr=-1&p=1&ps=30' \
'&js=var%20aUDOBatW={pages:(tp),data:%20(x)}' \
'&filter=(IsLatest=%27T%27)(enddate=^2018-09-30^)' \
'&rt=51098106'
base_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?'
headers = {
  'Host': 'data.eastmoney.com',
  'Referer': 'http://data.eastmoney.com/yjfp/201712.html',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
  # 'X-Requested-With': 'XMLHttpRequest',
}



class Handler(spider.FakeSpider):
  crawl_config = {
  }

  def on_start(self):
    self.crawl(self.url(), headers=self.header(), callback=self.processFirstPage)

  class InnerTask():
    def __init__(self, date, getTotalNumber=False):
      self._date = date
      self.getTotalNumber = getTotalNumber

    def dump(self):
      return {'data': self._date, 'getTotalNumber': self.getTotalNumber}

    def load(dict):
      return Handler.InnerTask(dict['data'], dict['getTotalNumber'])

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

    def genUrl(self, page):
      url = encode_params(self.genParams(page, self._date))
      return base_url + url


    def saveDB(self, data: pd.DataFrame, handler):
      def callback(result):
        handler.send_message(handler.project_name, result, self._date + '_' + result[KEY_NAME[ID_NAME]])

      re = util.saveMongoDB(data, util.genEmptyFunc(), DB_NAME, COLLECTION_HEAD + self._date, callback)
      util.everydayChange(re, 'yjyg')


  def url(self):
    return 'http://data.eastmoney.com/bbsj/201806/yjyg.html'

  def header(self):
    headers = {
      'Host': 'data.eastmoney.com',
      'Referer': 'http://data.eastmoney.com/yjfp/201712.html',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    return headers

  def processFirstPage(self, response):
    if response.ok == False:
      return

    data_list = response.doc('#date_type')
    # doc = pyquery.PyQuery(response)
    # data_list = doc('#sel_bgq')
    out = data_list.find('option')

    for one in out:
      print(one.text)
      year = float(one.text[:4])
      if year > 2017:
      # if one.text.startswith('2018'):
        innerTask = Handler.InnerTask(one.text)
        save = innerTask.dump()
        self.crawl(innerTask.genUrl(1), headers=self.header(), callback=self.processSecondPage, save=save)

  def processSecondPage(self, response):
    if response.ok == False:
      return

    content = response.content[13:]
    print(response.url)
    innerTask = Handler.InnerTask.load(response.save)
    try:
      data = content.decode('utf-8')
      print(data)
      data = data.replace('pages', '"pages"', 1)
      data = data.replace('data', '"data"', 1)
      json_data = json.loads(data)  # , encoding='GB2312')
      results = self.processDetailPage(json_data, innerTask)
      innerTask.saveDB(results, self)
    except UnicodeDecodeError as e:
      print(e)
    except Exception as e:
      print(e)

  def processDetailPage(self, json, innerTask):
    if json:

      total = json.get('pages')
      if innerTask.getTotalNumber == False:
        innerTask.getTotalNumber = True
        if total >= 2:
          save = innerTask.dump()
          for i in range(2, total + 1):
            self.crawl(innerTask.genUrl(i), headers=self.header(), callback=self.processSecondPage,
                       save=save)

      items = json.get('data')
      return self.parse_page(items)


  def parse_page(self, json):

    try:
      tmp = []
      for item in json:
        one_stock = util.utils.dealwithData(item, util.utils.threeOP(DATA_SUB,
                                                                     NEED_TO_NUMBER, KEY_NAME))
        one_stock[MONGODB_ID] = item.get(ID_NAME)
        series = pd.Series(one_stock)
        tmp.append(series)

      df = pd.DataFrame(tmp)
      print(df)
      return df
    except Exception as e:
      print(e)

  def on_message(self, project, msg):
    return msg



if __name__ == '__main__':
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()
