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
  sys.path.append('C:/workspace/code/self/github/py-code/ald')
  
##########################
import util


from spiders import spider


# MONGODB_ID = const.MONGODB_ID
# ID_NAME = const.CWSJ_KEYWORD.ID_NAME
# DB_NAME = const.CWSJ_KEYWORD.DB_NAME
# COLLECTION_HEAD = const.CWSJ_KEYWORD.COLLECTION_HEAD
# KEY_NAME = const.CWSJ_KEYWORD.KEY_NAME
# NEED_TO_NUMBER = const.CWSJ_KEYWORD.NEED_TO_NUMBER
# DATA_SUB = const.CWSJ_KEYWORD.DATA_SUB
# STOCK_LIST = setting.currentStockList()



class Handler(spider.FakeSpider):
  crawl_config = {
  }
  DB_NAME = "ald"
  COLLECTION_NAME = 'zb'
  CHINESE_NAME = '总榜'
  post = {
    "type": 0,
    "typeid": 0,
    "date": 1,
    "size": 50,
    "token": "",
  
  }
  url = 'https://zhishuapi.aldwx.com/Main/action/Dashboard/Homepage/data_list'
  

  def on_start(self):
    
    self.crawl(self.url, headers=self.header(), post=self.PostParams(), callback=self.processFirstPage)



  def header(self):
    headers = {
      #    """
      "authority": "zhishuapi.aldwx.com",
      #:method: POST
      #:path: /Main/action/Dashboard/Homepage/data_list
      #:scheme: https
      "accept": "application/json, text/plain, */*",
      "accept-encoding": "gzip, deflate, br",
      "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
  
      "content-type": "application/x-www-form-urlencoded",
      "origin": "http://www.aldzs.com",
      # user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
      #     """
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    
    }
    return headers
  
  
  def PostParams(self):
    return self.post
    pass
  

  def saveDB(self, data: pd.DataFrame):
    # def callback(result):
    #   self.send_message(self.project_name, result, key + '_' + result[MONGODB_ID])
    util.saveMongoDB(data, util.genEmptyFunc(), self.DB_NAME, self.COLLECTION_NAME, None)


  def processFirstPage(self, response):
    if response.ok == False:
      return

    data = response.content.decode('utf-8')
    json_data = json.loads(data)
    result = self.parse_page(json_data['data'])
    #save = response.save
    self.saveDB(result)


  def parse_page(self, json):
    try:
      tmp = []
      index = 1
      for item in json:
        item['_id'] = item.get('appkey')
        item['index'] = index
        series = pd.Series(item)
        tmp.append(series)
        index += 1

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


if __name__ == '__main__':
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()
