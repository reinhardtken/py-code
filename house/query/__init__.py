# -*- coding: utf-8 -*-

# sys
import datetime

# thirdpart
import pandas as pd
from pymongo import MongoClient

# this project
if __name__ == '__main__':
  import sys

##########################



def queryTop(top):
  client = MongoClient()
  db = client['house']
  collection = db['beijing']

  out = []

  cursor = collection.find()
  index = 0
  for c in cursor:
    out.append(c)
    index += 1
    if top != -1 and index > top:
      break

  if len(out):
    df = pd.DataFrame(out)
    return df
  else:
    return None



def queryTopDistrict(top, d):
  client = MongoClient()
  db = client['house']
  collection = db['beijing']

  out = []

  cursor = collection.find({'district': d})
  index = 0
  for c in cursor:
    out.append(c)
    index += 1
    if top != -1 and index > top:
      break

  if len(out):
    df = pd.DataFrame(out)
    return df
  else:
    return None

if __name__ == '__main__':
  df = queryTop(-1)
  df = queryTopDistrict(-1, '东城')
  print(df)
  df.to_excel('/home/ken/workspace/tmp/house.xls')
  # SaveData(re)
  pass
