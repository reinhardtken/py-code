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
    name = 'zy-esf-digest'

    src = 'zy'
    allowed_domains = [
      'sz.centanet.com',
                       ]
    start_urls = [
      'https://sz.centanet.com/ershoufang',
    ]
    head = 'https://sz.centanet.com'


    dbName = 'house'
    collectionName = 'zyPriceTrend'
    xpath = {

      'districts': '/html/body/div[4]/div/div[1]/div[1]/p[2]/a',
      'districtName': '/html/body/div[4]/div/div[1]/div[1]/p[2]/span[@class="curr"]/text()',
      'city': '/html/body/div[3]/div/a/text()',

      #   'lists': '//*[@id="ShowStyleByTable"]/li',
      # 
      # 'nextPageText': '//*[@id="esfList"]/div[4]/div[2]/div/div/div/div[last()]/a/text()',
      # 'nextPage': '//*[@id="esfList"]/div[4]/div[2]/div/div/div/div[last()]/a/@href',
      # 'nextPageText2': '//*[@id="esfList"]/div[4]/div[2]/div/div/div/div[last()]/text()',
      # 'nextPage2': '//*[@id="esfList"]/div[4]/div[2]/div/div/div/div[last()]/@href',
      # 'allPage': '/html/body/div[3]/div[4]/div[2]/div/div/div/div[2]/ul/li[last()]/a/@href',
      # 'allPage2': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()-1]/@href',

      'anchor': '/html/body/div[7]/div/div/div/a',
    }

    received = set()

    def parseDistricts(self, response):
      out = []

      ones = response.xpath(self.xpath['districts'])
      for one in ones:
        urls = one.xpath('.//@href').extract()
        for url in urls:
          if url.startswith('http'):
            # out.append(url)
            pass
          else:
            out.append(self.head + url)

      return out

    def parseUpDown(self, response):
      path = [
        '/html/body/div[@class="portraitLayer "]/div/p',
        # '/html/body/div[@class="portraitLayer tiphide openHotTip"]/div/p',
      ]
      clazz = {
        'up': './span[@class="up"]/text()',
        'down': './span[@class="down"]/text()',
      }
      for one in path:
        p = response.xpath(one)
        for k, v in clazz.items():
          percent = util.String2Number(''.join(p.xpath(v).extract()).strip())
          if not np.isnan(percent):
            return (k, percent)

    def parse(self, response):
      self.received.add(response.url)

      if 'step' not in response.meta:
        districts = self.parseDistricts(response)
        realOut = set(districts) - self.received
        for one in realOut:
          yield Request(one, meta={'step': 0})


      if 'step' in response.meta:
        district = ''
        city = ''
        d = response.xpath(self.xpath['city']).extract()
        if len(d):
          city = d[0][:2]

        d = response.xpath(self.xpath['districtName']).extract()
        if len(d):
          district = d[0]

        updown = self.parseUpDown(response)
        if updown is not None:
          n = items.ZYHousePriceTrend()
          n['dbName'] = 'house'
          n['collectionName'] = 'zyPriceTrend'
          n['city'] = city
          n['src'] = self.src
          n['district'] = district
          n['updown'] = updown[0]
          n['percent'] = updown[1]
          try:
            n['_id'] = str(util.getWeekofYear()) + '_' + city + '_' + district
          except Exception as e:
            print(e)
          yield n


