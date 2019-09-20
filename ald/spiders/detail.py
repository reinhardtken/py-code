# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime

import scrapy
import pymongo
from pymongo import MongoClient

import items
import util


class Spider(scrapy.Spider):
  name = 'ald-detail'
  
  allowed_domains = [
    'www.aldzs.com',
  ]
  start_urls = [
  
  ]
  head = 'http://www.aldzs.com'
  
  dbName = 'ald'
  collectionName = 'detail'
  srcCollectionName = 'game'
  xpath = {

  }
  
  received = set()
  
  
  def __init__(self):
    #http://www.aldzs.com/apps/?id=88691116&activetype=assistant
    #从db读取url
    client = MongoClient()
    db = client[self.dbName]
    collection = db[self.srcCollectionName]

    out = []

    cursor = collection.find()
    for c in cursor:
      url = "http://www.aldzs.com/apps/?id={0}&activetype=assistant".format(c["id"])
      out.append(url)
      
    self.start_urls = out[:]
  
  
  
  def parse(self, response):
    self.received.add(response.url)

    one = items.DetailItem()
    index = response.url.find('id=')
    if index != -1:
      index2 = response.url.find('&', index + 3)
      if index != -1:
        one['_id'] = response.url[index+3:index2]
      
    
    
    one['logo'] = util.ExtractString(response, '//*[@id="logo"]/@src')
    one['detail'] = util.ExtractString(response, '//*[@id="detail_page"]/div/div[2]/div[2]/div[5]/div[4]/text()').strip()
    array = response.xpath('//*[@id="detail_page"]/div/div[2]/div[2]/div[5]/div[2]/ul/li')
    tmpArray = []
    for tmp in array:
      t = util.ExtractString(tmp, './/img/@src')
      tmpArray.append(t)
    one['imageList'] = tmpArray
    yield one
    


