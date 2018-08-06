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
KEY_NAME = const.CWSJ_KEYWORD.KEY_NAME


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
  def string2Datetime(x):
    print(type(x))
    print(dir(x))
    return x.to_pydatetime()
    # return datetime.datetime.strptime(x, '%Y/%m/%d')

  df = pd.read_excel('/home/ken/workspace/tmp/im_out-adjust-000725(7).xlsx')
  df.loc[:, KEY_NAME['date']] = df.loc[:, KEY_NAME['date']].map(string2Datetime)
  df.set_index(KEY_NAME['date'], inplace=True)
  print(df)
  return df


if __name__ == '__main__':
  mock000725()
  pass
