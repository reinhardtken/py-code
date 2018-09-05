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
    name = 'lianjia-cj-digest'
    allowed_domains = [
      'lianjia.com',
                       ]
    start_urls = [
      'https://bj.lianjia.com/chengjiao/',
      'https://sh.lianjia.com/chengjiao/',
      'https://sz.lianjia.com/chengjiao/',
      'https://gz.lianjia.com/chengjiao/',
      'https://hz.lianjia.com/chengjiao/',
      'https://nj.lianjia.com/chengjiao/',
      'https://cs.lianjia.com/chengjiao/',
      'https://wh.lianjia.com/chengjiao/',
      'https://tj.lianjia.com/chengjiao/',
      'https://zz.lianjia.com/chengjiao/',
      'https://xa.lianjia.com/chengjiao/',
      'https://cd.lianjia.com/chengjiao/',
      'https://hf.lianjia.com/chengjiao/',
      'https://su.lianjia.com/chengjiao/',
      'https://cq.lianjia.com/chengjiao/',
      'https://xm.lianjia.com/chengjiao/',
    ]
    # head = 'https://sh.lianjia.com'
    dbName = 'house-cj'
    collectionName = 'digest'
    xpath = {
      'digest': '/html/body/div[5]/div[1]/div[2]/div[1]/span',
      'digestText': '/html/body/div[5]/div[1]/div[2]/div[1]',
      # 'digest': '/html/body/div[1]/div/div[5]/div[2]/ul/li',
    }


    def parse(self, response):
      oneOut = items.LianjiaTurnoverHouseDigest()
      ones = response.xpath(self.xpath['digest'])
      for one in ones:
        one = ''.join(one.xpath('./text()').extract()).strip()
        oneOut['house'] = String2Number(one)
        break

      ones = response.xpath(self.xpath['digestText'])
      for one in ones:
        one = ''.join(one.xpath('./text()').extract()).strip()
        oneOut['city'] = one[-6:-4]
        oneOut['_id'] = todayString() + '_' + oneOut['city']
        yield oneOut
        break
