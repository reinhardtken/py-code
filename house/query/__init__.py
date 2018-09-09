# -*- coding: utf-8 -*-

# sys
import datetime
import re

# thirdpart
import pandas as pd
import pymongo
from pymongo import MongoClient
import numpy as np

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/house')
##########################
import const



def test():
  client = MongoClient()
  db = client['house-cj']
  collection = db['beijing']

  cursor = collection.find()
  for c in cursor:
    title = c['title']
    tmp = title.strip().split(' ')
    building = None
    houseType = None
    square = None
    if len(tmp) > 0:
      building = tmp[0]
      if len(tmp) > 1:
        houseType = tmp[1]
        if len(tmp) > 2:
          square = String2Number(tmp[2])
          unitPrice = c['bidPrice'] / square
          re = {'$set': {'building': building, 'houseType': houseType, 'square': square, 'unitPrice': unitPrice}}
          print(re)
          collection.update_one({'_id': c['_id']}, re)



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


def queryTurnOverData(city, district, timeRange):
  client = MongoClient()
  db = client['house-cj']
  collection = db[city]

  out = []

  cursor = collection.find({'district': district, 'dealDate': {'$gte': timeRange[0], '$lt': timeRange[1]}}).sort('dealDate', pymongo.DESCENDING)
  for c in cursor:
    out.append(c)

  if len(out):
    df = pd.DataFrame(out)
    return df


def querySecondHandData(city, src):
  client = MongoClient()
  db = client['house']
  collection = db[city]

  out = []

  cursor = collection.find({'src': src})
  for c in cursor:
    out.append(c)

  if len(out):
    df = pd.DataFrame(out)
    return df


def test():
  client = MongoClient()
  db = client['house']
  collection = db['detail_digest']

  out = []

  total = 0
  cursor = collection.find({'src': 'zy', 'city': '深圳'})
  for c in cursor:
    total += c['number']

  if len(out):
    df = pd.DataFrame(out)
    return df

def createIndex():
  client = MongoClient()
  db = client['house-cj']
  collection = db['beijing']
  print(dir(collection))
  # collection.create_index([('distrcit', pymongo.TEXT)])
  # re = collection.create_index([('dealDate', pymongo.DESCENDING)])


  out = collection.list_indexes()
  for one in out:
    print(one)
  print(out)



def addSrc(city, src):
  client = MongoClient()
  db = client['house']
  collection = db[city]
  out = []
  cursor = collection.find()
  for c in cursor:
    if 'src' not in c:
      out.append(c)


  for data in out:
    data['src'] = src
    try:
      update_result = collection.update_one({'_id': data['_id']},
                                                 {'$set': data})

      if update_result.matched_count > 0 and update_result.modified_count > 0:
        # print('update to Mongo: %s : %s' % (self.dbName, self.collectionName))
        pass

      elif update_result.upserted_id is not None:
        # print('insert to Mongo: %s : %s : %s' % (self.dbName, self.collectionName, update_result.upserted_id))
        pass

    except pymongo.errors.DuplicateKeyError as e:
      pass
      # print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (self.dbName, self.collectionName, data['_id']))
    except Exception as e:
      print(e)



def test(city):
  client = MongoClient()
  db = client['house-trend']
  collection = db[city]
  out = []
  cursor = collection.find()
  for c in cursor:
    out.append(c)



  for data in out:
    date = data['crawlDate']
    iso = date.isocalendar()
    data['weekofYear'] = int(iso[0])*100 + int(iso[1])
    try:
      update_result = collection.update_one({'_id': data['_id']},
                                                 {'$set': data})

      if update_result.matched_count > 0 and update_result.modified_count > 0:
        # print('update to Mongo: %s : %s' % (self.dbName, self.collectionName))
        pass

      elif update_result.upserted_id is not None:
        # print('insert to Mongo: %s : %s : %s' % (self.dbName, self.collectionName, update_result.upserted_id))
        pass

    except pymongo.errors.DuplicateKeyError as e:
      pass
      # print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (self.dbName, self.collectionName, data['_id']))
    except Exception as e:
      print(e)


def queryCityPriceTrend(city, src, week=None):
  client = MongoClient()
  db = client['house-trend']
  collection = db[city]

  out = []
  cursor = None
  if week is None:
    cursor = collection.find({'src': src})
  else:
    cursor = collection.find({'src': src, 'weekofYear': week})
  for c in cursor:
    out.append(c)

  if len(out):
    df = pd.DataFrame(out)
    return df


if __name__ == '__main__':
  citys = const.CITYS
  for city in citys:
    addSrc(city, 'lj')
    pass
    # genCityPriceTrendDigest(city, 201836)
    # test(city)
  # createIndex()
  # test()
  pass
