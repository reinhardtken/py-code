# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import datetime
import re

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

class MongoPipeline(object):
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

    self.processor = self.choseProcessor(spider.name)

  def choseProcessor(self, name):
    if name.startswith('lianjia-cj-'):
      return self.processTurnoverData
    elif name.startswith('lianjia-'):
      return self.processSecondhandData

  def processTurnoverData(self, item):
    if np.isnan(item['bidPrice']) or item['bidPrice'] < 10:
      # 最近一个月成交，缺少具体数据
      pass
    else:
      try:
        item['diffPricePercent'] = (item['askPrice'] - item['bidPrice']) / item['askPrice']
        item['dealDate'] = datetime.datetime.strptime(item['dealDate'], '%Y.%m.%d')

        title = item['title']
        tmp = title.strip().split(' ')
        item['building'] = None
        item['houseType'] = None
        item['square'] = None
        if len(tmp) > 0:
          item['building'] = tmp[0]
          if len(tmp) > 1:
            item['houseType'] = tmp[1]
            if len(tmp) > 2:
              item['square'] = String2Number(tmp[2])
              item['unitPrice'] = item['bidPrice'] / item['square']
      except Exception as e:
        logging.warning("processTurnoverData Exception %s" % (str(e)))
      self.updateMongoDB(item)

  def processSecondhandData(self, item):
    self.updateMongoDB(item)

  def process_item(self, item, spider):
    if isinstance(item, items.LianjiaHouseItem) or isinstance(item, items.LianjiaTurnoverHouseItem):
      self.processor(item)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()

  def updateMongoDB(self, data):
    # print('enter updateMongoDB')
    try:
      update_result = self.collection.update_one({'_id': data['_id']},
                                                 {'$set': data}, upsert=True)

      if update_result.matched_count > 0 and update_result.modified_count > 0:
        print('update to Mongo: %s : %s' % (self.dbName, self.collectionName))

      elif update_result.upserted_id is not None:
        print('insert to Mongo: %s : %s : %s' % (self.dbName, self.collectionName, update_result.upserted_id))

    except pymongo.errors.DuplicateKeyError as e:
      print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (self.dbName, self.collectionName, data['_id']))
    except Exception as e:
      print(e)
    # print('leave updateMongoDB')

class MongoPipelineDigest(object):

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

  def updateMongoDB(self, data):
    # print('enter updateMongoDB')
    try:
      update_result = self.collection.update_one({'_id': data['_id']},
                                                 {'$set': data}, upsert=True)

      if update_result.matched_count > 0 and update_result.modified_count > 0:
        print('update to Mongo: %s : %s' % (self.dbName, self.collectionName))

      elif update_result.upserted_id is not None:
        print('insert to Mongo: %s : %s : %s' % (self.dbName, self.collectionName, update_result.upserted_id))

    except pymongo.errors.DuplicateKeyError as e:
      print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (self.dbName, self.collectionName, data['_id']))
    except Exception as e:
      print(e)
    # print('leave updateMongoDB')


class MongoPipelineDetailDigest(object):

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
    if isinstance(item, items.LianjiaHouseDetailDigest):
      self.updateMongoDB(item)
      raise scrapy.exceptions.DropItem()

    return item

  def close_spider(self, spider):
    self.client.close()

  def updateMongoDB(self, data):
    # print('enter updateMongoDB')
    try:
      update_result = self.collection.update_one({'_id': data['_id']},
                                                 {'$set': data}, upsert=True)

      if update_result.matched_count > 0 and update_result.modified_count > 0:
        print('update to Mongo: %s : %s' % (self.dbName, self.collectionName))

      elif update_result.upserted_id is not None:
        print('insert to Mongo: %s : %s : %s' % (self.dbName, self.collectionName, update_result.upserted_id))

    except pymongo.errors.DuplicateKeyError as e:
      print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (self.dbName, self.collectionName, data['_id']))
    except Exception as e:
      print(e)
    # print('leave updateMongoDB')