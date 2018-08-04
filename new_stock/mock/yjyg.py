# -*- coding: utf-8 -*-


# sys
import datetime

# thirdpart
import pandas as pd
from pymongo import MongoClient

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const

STOCK_LIST = const.STOCK_LIST
KEY_NAME = const.YJYG_KEYWORD.KEY_NAME


def QueryTop(top, code):
  client = MongoClient()
  db = client['stock']
  collection = db['cwsj-' + code]

  out = []

  cursor = collection.find()
  index = 0
  for c in cursor:
    c[KEY_NAME['date']] = datetime.datetime.strptime(c[KEY_NAME['date']], '%Y-%m-%d')
    out.append(c)
    print(c)
    index += 1
    if top != -1 and index > top:
      break

  df = pd.DataFrame(out)
  df.set_index(KEY_NAME['date'], inplace=True)
  return df


def mock000725():
  mock = [
    {
      "季度": datetime.datetime.strptime('2018-06-30', '%Y-%m-%d'),
      '代码': '000725',
      '名称': 'jdf',
      '预计净利润下限': 2,
      '预计净利润上限': 3,
      'forecastQuarter': 0.073250558,
    },
    {
      "季度": datetime.datetime.strptime('2017-12-31', '%Y-%m-%d'),
      '代码': '000725',
      '名称': 'jdf',
      '预计净利润下限': 2,
      '预计净利润上限': 3,
      'forecast': 0.229688476,
      'forecastQuarter': 0.167688476,
    },
    {
      "季度": datetime.datetime.strptime('2017-09-30', '%Y-%m-%d'),
      '代码': '000725',
      '名称': 'jdf',
      '预计净利润下限': 2,
      '预计净利润上限': 3,
      'forecast': 0.164063197,
      'forecastQuarter': 0.110063197

    },
    {
      "季度": datetime.datetime.strptime('2017-06-30', '%Y-%m-%d'),
      '代码': '000725',
      '名称': 'jdf',
      '预计净利润下限': 2,
      '预计净利润上限': 3,
      'forecastQuarter': 0.062250558

    },

  ]
  tmp = KEY_NAME.values()
  c = []
  for one in tmp:
    c.append(one)
  print(dir(tmp))
  c.append('forecast')
  c.append('forecastQuarter')
  df = pd.DataFrame(data=mock, columns=c)
  df.set_index(KEY_NAME['date'], inplace=True)
  print(df)
  return df


if __name__ == '__main__':
  mock000725()
  pass
