# -*- coding: utf-8 -*-

# sys
import datetime
import re
import traceback

# thirdpart
import pandas as pd
import pymongo
from pymongo import MongoClient
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter
from pymongo import MongoClient
from pymongo import errors

#this project
import query
import util
import const

def getWeekofYear():
  iso = datetime.datetime.now().isocalendar()
  return int(iso[0]) * 100 + int(iso[1])


def String2Number(s):
  out = np.nan
  try:
    out = float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])
  except Exception as e:
    pass

  return out


def SaveMongoDB(data, dbName, collectionName):
  client = MongoClient()
  db = client[dbName]
  collection = db[collectionName]
  result = data
  
  try:
    update_result = collection.update_one({'_id': result['_id']},
                                          {'$set': result})  # , upsert=True)
    
    if update_result.matched_count > 0:
      print('upate to Mongo: %s : %s' % (dbName, collectionName))
      if update_result.modified_count > 0:
        # detail[k] = result
        pass
    
    if update_result.matched_count == 0:
      try:
        if collection.insert_one(result):
          print('insert to Mongo: %s : %s' % (dbName, collectionName))
          # detail[k] = result
      except errors.DuplicateKeyError as e:
        print('faild to Mongo!!!!: %s : %s' % (dbName, collectionName))
        pass
  
  except Exception as e:
    print(e)
    
    
def QueryHS300All():
  client = MongoClient()
  db = client['stock']
  collection = db['hs300_stock_list']

  out = []

  cursor = collection.find()
  for c in cursor:
    out.append(c)

  if len(out):
    df = pd.DataFrame(out)
    df.set_index(const.HS300.KEY_NAME['code'], inplace=True)
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
    out.append(c[const.HS300.KEY_NAME['code']])

  return out



def QueryAll():
  client = MongoClient()
  db = client['stock']
  collection = db['stock_list']

  out = []

  cursor = collection.find()
  for c in cursor:
    out.append(c)

  if len(out):
    df = pd.DataFrame(out)
    df.set_index("代码", inplace=True)
    return df
  else:
    return None
  
  
def PrintException(e):
  msg = traceback.format_exc()
  print(msg)



def LoadData(dbName, collectionName, condition={}, sort=[('_id', 1)]):
  client = MongoClient()
  db = client[dbName]
  collection = db[collectionName]
  cursor = collection.find(condition).sort(sort)
  out = []
  for c in cursor:
    out.append(c)

  if len(out):
    df = pd.DataFrame(out)
    # df.drop('date', axis=1, inplace=True)
    df.set_index('_id', inplace=True)
    return df

  return None


def LoadData2(dbName, collectionName, codes):
  client = MongoClient()
  db = client[dbName]
  collection = db[collectionName]
  out = []
  for code in codes:
    cursor = collection.find({'_id': code})
    for c in cursor:
      out.append(c)
      break

  if len(out):
    df = pd.DataFrame(out)
    try:
      df.drop('name', axis=1, inplace=True)
    except Exception as e:
      pass
    df.set_index('_id', inplace=True)
    return df

def LastPriceNone(codes):
  client = MongoClient()
  
  out = []
  for code in codes:
    db = client['stock_all_kdata_none']
    collection = db[code]
    cursor = collection.find().sort([('_id', -1)]).limit(1)
    for c in cursor:
      out.append({'_id': code, 'price': c['close']})
      break

  if len(out):
    df = pd.DataFrame(out)
    df.set_index('_id', inplace=True)
    return df


  return None