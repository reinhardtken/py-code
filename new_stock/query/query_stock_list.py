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
import const.TS as TS



def queryAll():
  client = MongoClient()
  db = client['stock']
  collection = db['stock_list']

  out = []

  cursor = collection.find()
  index = 0
  for c in cursor:
    out.append(c)

  if len(out):
    df = pd.DataFrame(out)
    df.set_index(const.TS.BASICS.KEY_NAME['code'], inplace=True)
    return df
  else:
    return None



def queryOne(code):
  client = MongoClient()
  db = client['stock']
  collection = db['stock_list']

  out = []

  cursor = collection.find({const.TS.BASICS.KEY_NAME['code']: code})

  for c in cursor:
    df = pd.Series(c)
    # df.set_index(const.TS.BASICS.KEY_NAME['code'], inplace=True)
    return df
  else:
    return None


def queryZgb(code):
  one = queryOne(code)
  if one is not None:
    return one[const.TS.BASICS.KEY_NAME['zgb']]

if __name__ == '__main__':
  re = queryZgb('002415')
  pass
