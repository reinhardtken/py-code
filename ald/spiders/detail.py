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
from spiders import toplist_dict


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
  
  xpath = {

  }
  
  received = set()
  
  
  def __init__(self):
    #http://www.aldzs.com/apps/?id=88691116&activetype=assistant
    #从db读取url
    # self.srcCollectionName = c
    client = MongoClient()
    db = client[self.dbName]
    data = toplist_dict.GetList()

    out = []
    for one in data:
      collection = db[one['key']]
      cursor = collection.find()
      for c in cursor:
        url = "http://www.aldzs.com/apps/?id={0}&activetype=assistant".format(c["id"])
        print(url)
        out.append(url)
      
    self.start_urls = out[:]
  
  
  
  def parse(self, response):
    self.received.add(response.url)
    print("receive data...  " + response.url)

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
    


