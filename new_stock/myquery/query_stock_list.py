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
  for c in cursor:
    out.append(c)

  if len(out):
    df = pd.DataFrame(out)
    df.set_index(const.TS.BASICS.KEY_NAME['code'], inplace=True)
    return df
  else:
    return None


def queryAllCode():
  client = MongoClient()
  db = client['stock']
  collection = db['stock_list']

  out = []

  cursor = collection.find()
  for c in cursor:
    out.append(c["_id"])

  return out


def queryOne(code):
  client = MongoClient()
  db = client['stock']
  collection = db['stock_list']

  cursor = collection.find({const.TS.BASICS.KEY_NAME['code']: code})

  for c in cursor:
    df = pd.Series(c)
    # df.set_index(const.TS.BASICS.KEY_NAME['code'], inplace=True)
    return df
  else:
    return None


def queryOneWrapper(code):
  re = queryOne(code)
  tryAgain = False
  if re is not None:
    try:
      zgb = re[const.TS.BASICS.KEY_NAME['zgb']]
    except KeyError as e:
      import fake_spider.zgb3
      tryAgain = True
      fake_spider.zgb3.runOne([code])

  if tryAgain:
    re = queryOne(code)
  return re
  


def queryZgb(code):
  one = queryOne(code)
  if one is not None:
    return one[const.TS.BASICS.KEY_NAME['zgb']]

if __name__ == '__main__':
  re = queryZgb('002415')
  pass
