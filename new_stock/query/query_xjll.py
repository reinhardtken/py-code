# -*- coding: utf-8 -*-


# sys
import datetime

# thirdpart
import pandas as pd
import pymongo
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
KEY_NAME = const.XJLL_KEYWORD.KEY_NAME


def QueryTop(top, code):
  client = MongoClient()
  db = client['stock']
  collection = db['xjll-' + code]

  out = []

  cursor = collection.find().sort(KEY_NAME['reportdate'], pymongo.DESCENDING)
  index = 0
  for c in cursor:
    c[KEY_NAME['reportdate']] = datetime.datetime.strptime(c[KEY_NAME['reportdate']], '%Y-%m-%d')
    out.append(c)
    print(c)
    index += 1
    if top != -1 and index > top:
      break

  df = pd.DataFrame(out)
  try:
    df.set_index(KEY_NAME['reportdate'], inplace=True)
  except KeyError as e:
    print(e)
  print(df)
  return df



if __name__ == '__main__':
  pass
