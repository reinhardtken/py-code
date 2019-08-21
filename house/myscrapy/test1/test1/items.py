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



class LianjiaHouseAllInfoItem(scrapy.Item):
  # https://dianpu.lianjia.com/1000000020119665
  # https://bj.lianjia.com/chengjiao/101102573287.html
  # https://bj.lianjia.com/ershoufang/101104120051.html
  # https://bj.lianjia.com/chengjiao/101103200411.html
  title = scrapy.Field()
  _id = scrapy.Field()

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

#小区信息
class BlockItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  name = scrapy.Field()  # //*[@id="sem_card"]/div/div[1]/div[1]/div/a[1]
  block = scrapy.Field()  # //*[@id="sem_card"]/div/div[1]/div[1]/div/span

  price = scrapy.Field()#//*[@id="sem_card"]/div/div[1]/div[2]/div[1]/a
  sellCounter = scrapy.Field()#//*[@id="sem_card"]/div/div[1]/div[2]/div[2]/div[2]
  traded = scrapy.Field()#//*[@id="sem_card"]/div/div[1]/div[2]/div[3]/a
  lookCounter = scrapy.Field()#//*[@id="sem_card"]/div/div[1]/div[2]/div[4]/div[2]
  crawlDate = scrapy.Field()

#房屋详细信息
class HouseItem2(scrapy.Item):
  src = scrapy.Field()

  title = scrapy.Field()#/html/body/div[3]/div/div/div[1]/h1
  #这个是链家编号+crawldate
  #/html/body/div[5]/div[2]/div[6]/div[4]/span[2]
  _id = scrapy.Field() #/html/body/div[5]/div[2]/div[6]/div[4]/span[2]
  #这个是真实的链家编号
  houseID = scrapy.Field()
  # block = scrapy.Field()



  unitPrice = scrapy.Field()#/html/body/div[5]/div[2]/div[4]/div[1]/div[1]/span
  totalPrice = scrapy.Field()#/html/body/div[5]/div[2]/div[4]/span[1]

  # houseInfo = scrapy.Field()
  community = scrapy.Field()
  houseType = scrapy.Field()#/html/body/div[5]/div[2]/div[5]/div[1]/div[1]
  square = scrapy.Field()#/html/body/div[5]/div[2]/div[5]/div[3]/div[1]

  # positionInfo = scrapy.Field()
  level = scrapy.Field()#/html/body/div[5]/div[2]/div[5]/div[1]/div[2]
  structure = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[1]/span

  thb = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[10]/span
  lx = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[6]/span
  heating = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[11]/span
  property = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[13]/span
  # property = scrapy.Field()  # /html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[13]/span

  attention = scrapy.Field()#//*[@id="favCount"]
  follow = scrapy.Field()#//*[@id="cartCount"]
  release = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[1]/span[2]
  lastTrade = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[3]/span[2]
  years = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[5]/span[2]
  mortgage = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[7]/span[2]


  ownership = scrapy.Field()#/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[2]/span[2]
  use = scrapy.Field()  #/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[4]/span[2]
  propertyRight = scrapy.Field()  #/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[6]/span[2]
  book = scrapy.Field()  #/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[8]/span[2]

  crawlDate = scrapy.Field()
  pass

