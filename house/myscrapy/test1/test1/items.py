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


class DBHead(scrapy.Item):
  dbName = scrapy.Field()
  collectionName = scrapy.Field()

class ZYHousePriceTrend(DBHead):
  city = scrapy.Field()
  _id = scrapy.Field()
  src = scrapy.Field()
  district = scrapy.Field()
  updown = scrapy.Field()
  percent = scrapy.Field()
