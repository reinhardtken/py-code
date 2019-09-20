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




def run():
  DB_NAME = 'ald'
  COLLECTION_NAME = 'toplist_dict'
  data = [
    {
      'key': 'content',
      'name': '内容资讯',
    },
    {
      'key':  'camera',
      'name': '图片摄影',
    },
    {
      'key': 'game',
      'name': '游戏',
    },
    {
      'key': 'life',
      'name': '生活服务',
    },
    {
      'key': 'shopping',
      'name': '网络购物',
    },
    {
      'key': 'social',
      'name': '社交',
    },
    {
      'key': 'tools',
      'name': '工具',
    },
  ]

  tmp = []
  
  for item in data:
    item['_id'] = item['key']
    series = pd.Series(item)
    tmp.append(series)

  df = pd.DataFrame(tmp)
  util.saveMongoDB(df, util.genEmptyFunc(), DB_NAME, COLLECTION_NAME, None)


if __name__ == '__main__':
  run()