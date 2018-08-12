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



def QueryAll():
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
    df.set_index(const.TS.KEY_NAME['code'], inplace=True)
    return df
  else:
    return None


def QueryCodeList():
  client = MongoClient()
  db = client['stock']
  collection = db['hs300_stock_list']

  out = []

  cursor = collection.find()
  index = 0
  for c in cursor:
    out.append(c[TS.HS300.KEY_NAME['code']])

  return out




if __name__ == '__main__':
  QueryCodeList()
  pass
