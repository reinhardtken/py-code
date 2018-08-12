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



def QueryLastKData(code):
  client = MongoClient()
  db = client['stock_kdata']
  collection = db[code]

  out = []

  cursor = collection.find().sort('date', pymongo.DESCENDING)

  for c in cursor:
    out.append(c)
    break

  if len(out):
    df = pd.DataFrame(out)
    df.set_index(const.TS.BASICS.KEY_NAME['code'], inplace=True)
    return df
  else:
    return None



if __name__ == '__main__':
  QueryLastKData('002415')
  pass
