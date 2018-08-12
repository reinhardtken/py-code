# -*- coding: utf-8 -*-

# sys
import datetime

# thirdpart
import pandas as pd
from pymongo import MongoClient
import pymongo

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const
import const.TS as TS



def queryLastKData(code):
  client = MongoClient()
  db = client['stock_kdata']
  collection = db[code]

  cursor = collection.find().sort('date', pymongo.DESCENDING)

  for c in cursor:
    df = pd.Series(c)
    return df
  else:
    return None


def queryLastClosePrice(code):
  one = queryLastKData(code)
  return one['close']



if __name__ == '__main__':
  queryLastKData('002415')
  pass
