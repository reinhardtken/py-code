# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime

import scrapy
from scrapy.http import Request
import numpy as np


import items
import util




class Spider(scrapy.Spider):
    name = 'ald-toplist'

    allowed_domains = [
      'www.aldzs.com',
                       ]
    start_urls = [
      'http://www.aldzs.com/toplist/?type=0&typeid=0&date=0&tabsactive=0',
    ]
    head = 'http://www.aldzs.com'
   
    dbName = 'ald'
    collectionName = 'toplist'
    xpath = {
        'lists': '//*[@id="default"]/div[5]/div[2]/div[2]/div[3]/div[2]/div/div[2]/div',
       
    }

    received = set()


    def parseOne(self, one, index):
      oneOut = items.TopListItem()
      
      try:
        oneOut['index'] = index
        oneOut['name'] = util.ExtractString(one, './/ul/li[3]/a/@title')
        oneOut['href'] = util.ExtractString(one, './/ul/li[3]/a/@href')
        if len(oneOut['href']):
          index = oneOut['href'].find('id=')
          if index != -1:
            oneOut['_id'] = oneOut['href'][index+3:] + '_zb'
        oneOut['kind'] = util.ExtractString(one, './/ul/li[4]/text()')
        oneOut['glgzhs'] = util.ExtractNumber(one, './/ul/li[5]/text()')
        oneOut['gshydl'] = util.ExtractString(one, './/ul/li[6]/text()')
        oneOut['czzs'] = util.ExtractNumber(one, './/ul/li[7]/text()')
        oneOut['aldzs'] = util.ExtractNumber(one, './/ul/li[8]/span/text()')
      
      except Exception as e:
        print(e)
        logging.warning("parseOne Exception %s"%(str(e)))
      return oneOut



    def parse(self, response):
      self.received.add(response.url)
      ones = response.xpath(self.xpath['lists'])

      index = 1
      for one in ones:
        oneOut = self.parseOne(one, index)
        yield oneOut
        index += 1
      
        
