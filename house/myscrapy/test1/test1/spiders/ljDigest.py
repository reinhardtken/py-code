# -*- coding: utf-8 -*-
import urllib
import logging
import datetime

import scrapy
from scrapy.http import Request
import items

def String2Number(s):
  import re
  return float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])

def todayString():
  now = datetime.datetime.now()
  now = now.replace(hour=0, minute=0, second=0, microsecond=0)
  return now.strftime('%Y-%m-%d')

class Spider(scrapy.Spider):
    name = 'lianjia-digest'
    allowed_domains = [
      'lianjia.com',
                       ]
    start_urls = [
      'https://bj.lianjia.com',
      'https://sh.lianjia.com',
      'https://sz.lianjia.com',
      'https://gz.lianjia.com',
      'https://hz.lianjia.com',
      'https://nj.lianjia.com',
      'https://cs.lianjia.com',
      'https://wh.lianjia.com',
      'https://tj.lianjia.com/',
      'https://zz.lianjia.com/',
      'https://xa.lianjia.com/',
      'https://cd.lianjia.com/',
      'https://hf.lianjia.com/',
      'https://su.lianjia.com/',
      'https://cq.lianjia.com/',
      'https://xm.lianjia.com/',
    ]
    # head = 'https://sh.lianjia.com'
    dbName = 'house'
    collectionName = 'digest'
    xpath = {
      'digest': '/html/body/div[1]/div/div[5]/div[2]/ul/li',
    }


    def parse(self, response):
      oneOut = items.LianjiaHouseDigest()
      ones = response.xpath(self.xpath['digest'])
      for one in ones:
        one = ''.join(one.xpath('./text()').extract()).strip()
        if one.find('新房') != -1:
          oneOut['newHouse'] = String2Number(one)
        elif one.find('二手房') != -1:
          oneOut['city'] = one[:2]
          oneOut['_id'] = todayString() + '_' + oneOut['city']
          oneOut['secondhandHouse'] = String2Number(one)
        elif one.find('租房') != -1:
          oneOut['rentHouse'] = String2Number(one)

      yield oneOut
