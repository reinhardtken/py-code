# -*- coding: utf-8 -*-

# sys
import datetime
import re

# thirdpart
# import pandas as pd
import pymongo
from pymongo import MongoClient
# import numpy as np
import datetime
#thirdpart
import pymongo
from pymongo import MongoClient
from pymongo import errors
# import pandas as pd
# import numpy as np

#this project


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






def ExtractString(response, path):
  re = response.xpath(path).extract()
  if isinstance(re, list) and len(re):
    return re[0]
  else:
    return re


def ExtractNumber(response, path):
  return String2Number(ExtractString(response, path))


def todayString():
  now = datetime.datetime.now()
  now = now.replace(hour=0, minute=0, second=0, microsecond=0)
  return now.strftime('%Y-%m-%d')



def today():
  now = datetime.datetime.now()
  now = now.replace(hour=0, minute=0, second=0, microsecond=0)
  return now



def saveMongoDB(data, keyFunc, dbName, collectionName, callback=None):
  client = MongoClient()
  db = client[dbName]
  collection = db[collectionName]

  out = {'db': dbName, 'collection': collectionName}
  detail = {}

  for v in data:
    result = v
    # print(dir(k))
    # result.update(keyFunc(k, result))

    try:
      if callback:
        callback(result)
    except Exception as e:
      print(e)
    try:
      update_result = collection.update_one({'_id': result['_id']},
                                          {'$set': result})#, upsert=True)

      if update_result.matched_count > 0:
        print('upate to Mongo: %s : %s'%(dbName, collectionName))
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

  # out['detail'] = detail
  print('leave saveMongoDB')
  return out



def genEmptyFunc():
  def emptyFunc(v, d):
    return {}

  return emptyFunc