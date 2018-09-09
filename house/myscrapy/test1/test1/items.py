# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    src = scrapy.Field()
    title = scrapy.Field()
    _id = scrapy.Field()
    district = scrapy.Field()
    subDistrict = scrapy.Field()
    # building = scrapy.Field()
    layout = scrapy.Field()
    unitPrice = scrapy.Field()
    totalPrice = scrapy.Field()

    # houseInfo = scrapy.Field()
    community = scrapy.Field()
    houseType = scrapy.Field()
    square = scrapy.Field()

    # positionInfo = scrapy.Field()
    level = scrapy.Field()
    structure = scrapy.Field()
    area = scrapy.Field()

    # followInfo = scrapy.Field()
    attention = scrapy.Field()
    follow = scrapy.Field()
    release = scrapy.Field()

    crawlDate = scrapy.Field()
    pass


class LianjiaHouseDigest(scrapy.Item):
    city = scrapy.Field()
    _id = scrapy.Field()
    newHouse = scrapy.Field()
    secondhandHouse = scrapy.Field()
    rentHouse = scrapy.Field()


class HouseDetailDigest(scrapy.Item):
  city = scrapy.Field()
  _id = scrapy.Field()
  src = scrapy.Field()
  district = scrapy.Field()
  subDistrict = scrapy.Field()
  number = scrapy.Field()

class LianjiaTurnoverHouseDigest(scrapy.Item):
    city = scrapy.Field()
    _id = scrapy.Field()
    house = scrapy.Field()
    # secondhandHouse = scrapy.Field()
    # rentHouse = scrapy.Field()


class LianjiaTurnoverHouseDetailDigest(scrapy.Item):
  city = scrapy.Field()
  _id = scrapy.Field()
  district = scrapy.Field()
  subDistrict = scrapy.Field()
  number = scrapy.Field()


class LianjiaTurnoverHouseItem(scrapy.Item):
  title = scrapy.Field()
  _id = scrapy.Field()
  href = scrapy.Field()
  district = scrapy.Field()
  subDistrict = scrapy.Field()

  askPrice = scrapy.Field()
  bidPrice = scrapy.Field()
  diffPricePercent = scrapy.Field()
  unitPrice = scrapy.Field()
  dealCycle = scrapy.Field()
  dealDate = scrapy.Field()

  building = scrapy.Field()
  houseType = scrapy.Field()
  square = scrapy.Field()
  pass


class LianjiaRentHouseItem(scrapy.Item):
  title = scrapy.Field()
  _id = scrapy.Field()

  district = scrapy.Field()
  subDistrict = scrapy.Field()



  rentPrice = scrapy.Field()

  # houseInfo = scrapy.Field()
  community = scrapy.Field()
  houseType = scrapy.Field()
  square = scrapy.Field()

  # positionInfo = scrapy.Field()
  level = scrapy.Field()
  structure = scrapy.Field()

  follow = scrapy.Field()
  release = scrapy.Field()



class LianjiaRentHouseDetailDigest(scrapy.Item):
  city = scrapy.Field()
  _id = scrapy.Field()
  district = scrapy.Field()
  subDistrict = scrapy.Field()
  number = scrapy.Field()


# class PriceTrend(scrapy.Item):
#   src = scrapy.Field()
#   houseID = scrapy.Field()
#   square = scrapy.Field()
#
#   district = scrapy.Field()
#   subDistrict = scrapy.Field()
#
#   newUnitPrice = scrapy.Field()
#   newTotalPrice = scrapy.Field()
#
#   oldUnitPrice = scrapy.Field()
#   oldTotalPrice = scrapy.Field()
#   trend = scrapy.Field()
#   diffPercent = scrapy.Field()
#   crawlDate = scrapy.Field()


# if __name__ == "__main__":
#   import logging
#   import datetime
#   import re
#   import math
#
#   import pymongo
#   import numpy as np
#   import scrapy.exceptions
#
#
#   def today():
#     now = datetime.datetime.now()
#     now = now.replace(hour=0, minute=0, second=0, microsecond=0)
#     return now
#
#
# #
#   out = PriceTrend()
#   out['houseID'] = '101103107361'
#   out['src'] = 'lj'
#   out['newUnitPrice'] = 113148.0
#   out['newTotalPrice'] = 568.0
#   out['oldUnitPrice'] = 590
#   out['oldTotalPrice'] = 117530.0
#   if out['newTotalPrice'] > out['oldTotalPrice']:
#     out['trend'] = 1
#   else:
#     out['trend'] = -1
#   out['crawlDate'] = today()
#   client = pymongo.MongoClient()
#   dbPriceTrend = client['house-trend']
#   collectionPriceTrend = dbPriceTrend['beijing']
#   tmp = {'crawlDate': datetime.datetime(2018, 9, 9, 0, 0),
#    'houseID': '101103107361',
#    'newTotalPrice': 568.0,
#    'newUnitPrice': 113148.0,
#    'oldTotalPrice': 590.0,
#    'oldUnitPrice': 117530.0,
#    'src': 'lj',
#    'trend': -1}
#   try:
#     insertResult = collectionPriceTrend.insert_one(tmp)
#   except pymongo.errors.DuplicateKeyError as e:
#     # print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (self.dbName, self.collectionName, data['house']))
#     pass
#   except Exception as e:
#     print(e)
