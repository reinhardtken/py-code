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
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()#//*[@id="sem_card"]/div/div[1]/div[1]/div/a[1]
    
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

class TopListItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  _id = scrapy.Field()
  index = scrapy.Field()
  name = scrapy.Field() 
  href = scrapy.Field()
  kind = scrapy.Field() #/ul/li[4]
  glgzhs = scrapy.Field() #/ul/li[5]
  gshydl = scrapy.Field()#/ul/li[6]
  czzs = scrapy.Field()#/ul/li[7]
  aldzs = scrapy.Field()#/ul/li[8]/span
  
  pass


class DetailItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  _id = scrapy.Field()
  logo = scrapy.Field()
  imageList = scrapy.Field()
  detail = scrapy.Field()

  