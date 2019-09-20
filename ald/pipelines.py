# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import datetime
import re
import math

import pymongo
import numpy as np
import scrapy.exceptions

import items


def String2Number(s):
  out = np.nan
  try:
    out = float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])
  except Exception as e:
    pass

  return out


def today():
  now = datetime.datetime.now()
  now = now.replace(hour=0, minute=0, second=0, microsecond=0)
  return now


class SaveMongoDB(object):

  def processPriceChange(self, data):
    out = None
    cursor = self.collection.find({'_id': data['_id']})
    for c in cursor:
      diff = math.fabs(data['totalPrice'] - c['totalPrice'])
      if diff > 1:
        out = {}  # items.PriceTrend()
        out['houseID'] = data['_id']
        out['src'] = data['src']
        out['district'] = data['district']
        out['subDistrict'] = data['subDistrict']
        out['square'] = data['square']
        out['newUnitPrice'] = data['unitPrice']
        out['newTotalPrice'] = data['totalPrice']
        out['oldUnitPrice'] = c['unitPrice']
        out['oldTotalPrice'] = c['totalPrice']
        out['diffPercent'] = diff / out['oldTotalPrice']
        if out['newTotalPrice'] > out['oldTotalPrice']:
          out['trend'] = 1
        else:
          out['trend'] = -1
        out['crawlDate'] = today()
        iso = out['crawlDate'].isocalendar()
        out['weekofYear'] = int(iso[0]) * 100 + int(iso[1])
      break

    return  out

  def updateMongoDB(self, data, collection=None, dbName=None, collectionName=None):
    # print('enter updateMongoDB')
    if collection is None:
      collection =self.collection
      dbName = self.dbName
      collectionName = self.collectionName
    out = None
    try:
      if isinstance(data, items.HouseItem):
        out = self.processPriceChange(data)

      update_result = collection.update_one({'_id': data['_id']},
                                                 {'$set': data}, upsert=True)

      if update_result.matched_count > 0 and update_result.modified_count > 0:
        print('update to Mongo: %s : %s' % (dbName, collectionName))

      elif update_result.upserted_id is not None:
        print('insert to Mongo: %s : %s : %s' % (dbName, collectionName, update_result.upserted_id))

    except pymongo.errors.DuplicateKeyError as e:
      print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (dbName, collectionName, data['_id']))
    except Exception as e:
      print(e)
    # print('leave updateMongoDB')
    return out

class MongoPipeline(SaveMongoDB):
  # def __init__(self, mongo_uri, mongo_db):
  #     self.mongo_uri = mongo_uri
  #     self.mongo_db = mongo_db

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    # self.dbName = 'house'
    # self.collectionName = 'beijing'
    self.dbName = spider.dbName
    self.collectionName = spider.collectionName
    self.db = self.client[self.dbName]
    self.collection = self.db[self.collectionName]
    self.dbPriceTrend = self.client['house-trend']
    self.collectionPriceTrend = self.dbPriceTrend[self.collectionName]

    self.processor = self.choseProcessor(spider.name)

  def choseProcessor(self, name):
    if name.find('-cj-') != -1:
      return self.processTurnoverData
    elif name.find('-esf-') != -1:
      return self.processSecondhandData

  def processTurnoverData(self, item):
      self.updateMongoDB(item)

  def processSecondhandData(self, item):
    out = self.updateMongoDB(item)
    if out is not None:
      self.processPriceTrendItem(out)


  def processPriceTrendItem(self, data):
    if isinstance(data, dict) and 'newTotalPrice' in data:
      try:
        insertResult = self.collectionPriceTrend.insert_one(data)
      except pymongo.errors.DuplicateKeyError as e:
        # print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (self.dbName, self.collectionName, data['house']))
        pass
      except Exception as e:
        print(e)


  def process_item(self, item, spider):
    if isinstance(item, items.HouseItem) or isinstance(item, items.LianjiaTurnoverHouseItem):
      self.processor(item)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()



class MongoPipelineDigest(SaveMongoDB):

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    self.dbName = 'house'
    self.collectionName = 'digest'
    self.db = self.client[self.dbName]
    self.collection = self.db[self.collectionName]


  def process_item(self, item, spider):
    if isinstance(item, items.LianjiaHouseDigest):
      self.updateMongoDB(item)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()




class MongoPipelineDetailDigest(SaveMongoDB):

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    self.dbName = 'house'
    self.collectionName = 'detail_digest'
    self.db = self.client[self.dbName]
    self.collection = self.db[self.collectionName]


  def process_item(self, item, spider):
    if isinstance(item, items.HouseDetailDigest):
      self.updateMongoDB(item)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()




class MongoPipelineTurnoverDigest(SaveMongoDB):

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    self.dbName = 'house-cj'
    self.collectionName = 'digest'
    self.db = self.client[self.dbName]
    self.collection = self.db[self.collectionName]


  def process_item(self, item, spider):
    if isinstance(item, items.LianjiaTurnoverHouseDigest):
      self.updateMongoDB(item)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()




class MongoPipelineTurnoverDetailDigest(SaveMongoDB):

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    self.dbName = 'house-cj'
    self.collectionName = 'detail_digest'
    self.db = self.client[self.dbName]
    self.collection = self.db[self.collectionName]


  def process_item(self, item, spider):
    if isinstance(item, items.LianjiaTurnoverHouseDetailDigest):
      self.updateMongoDB(item)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()


class MongoPipelineRentHouse(SaveMongoDB):

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    self.dbName = spider.dbName
    self.collectionName = spider.collectionName
    self.db = self.client[self.dbName]
    self.collection = self.db[self.collectionName]


  def process_item(self, item, spider):
    if isinstance(item, items.LianjiaRentHouseItem):
      self.updateMongoDB(item)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()


class MongoPipelineRentDetailDigest(SaveMongoDB):

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    self.dbName = 'house-zf'
    self.collectionName = 'detail_digest'
    self.db = self.client[self.dbName]
    self.collection = self.db[self.collectionName]


  def process_item(self, item, spider):
    if isinstance(item, items.LianjiaRentHouseDetailDigest):
      self.updateMongoDB(item)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()


class MongoPipelineRest(SaveMongoDB):

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    self.collectionMap = {}
    self.nameSet = set()


  def process_item(self, item, spider):
    if isinstance(item, items.DBHead):
      dbName = item['dbName']
      collectionName = item['collectionName']
      key = dbName + '_' + collectionName
      if key in self.nameSet:
        del item['dbName']
        del item['collectionName']
        self.updateMongoDB(item, self.collectionMap[key])
      else:
        collection = self.client[dbName][collectionName]
        self.collectionMap[key] = collection
        self.nameSet.add(key)
        del item['dbName']
        del item['collectionName']
        self.updateMongoDB(item, collection, dbName, collectionName)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()
    
    
    
class MongoPipelineALD(SaveMongoDB):

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    self.dbName = spider.dbName
    self.collectionName = spider.collectionName
    self.db = self.client[self.dbName]
    self.collection = self.db[self.collectionName]


  def process_item(self, item, spider):
    if isinstance(item, items.TopListItem):
      self.updateMongoDB(item)
      raise scrapy.exceptions.DropItem()

    return item


  def close_spider(self, spider):
    self.client.close()
    
    
    
class MongoPipelineALDDetail(SaveMongoDB):

  @classmethod
  def from_crawler(cls, crawler):
    # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    return cls()

  def open_spider(self, spider):
    self.client = pymongo.MongoClient()
    self.dbName = spider.dbName
    self.collectionName = spider.collectionName
    self.db = self.client[self.dbName]
    self.collection = self.db[self.collectionName]


  def process_item(self, item, spider):
    if isinstance(item, items.DetailItem):
      self.updateMongoDB(item)
      raise scrapy.exceptions.DropItem()

    return item


  def close_spider(self, spider):
    self.client.close()