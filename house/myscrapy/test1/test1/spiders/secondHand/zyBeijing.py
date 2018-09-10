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
import spiders.secondHand.zyShenzhen2

class Spider(spiders.secondHand.zyShenzhen2.Spider):
  name = 'zy-esf-bj'
  city = '北京'
  src = 'zy'
  allowed_domains = [
    'bj.centanet.com',
  ]
  start_urls = [
    'https://bj.centanet.com/ershoufang/',
  ]
  head = 'https://bj.centanet.com'

  collectionName = 'beijing'

# class Spider(spiders.secondHand.zyShanghai.Spider):
#   name = 'zy-esf-bj'
#   city = '北京'
#   src = 'zy'
#   allowed_domains = [
#     'bj.centanet.com',
#   ]
#   start_urls = [
#     'https://bj.centanet.com/ershoufang/chaoyangou/',
#   ]
#   head = 'https://bj.centanet.com'
#
#   nextPageOrder = -1
#   reversed = False
#   useAllPge = True
#   dbName = 'house'
#   collectionName = 'beijing'
#
#
#   def parseUpDown(self, response):
#     path = [
#       '/html/body/div[@class="portraitLayer tiphide closeHotTip"]/div/p',
#       '/html/body/div[@class="portraitLayer tiphide openHotTip"]/div/p',
#     ]
#     clazz = {
#       'up': '/span[@class="up"]/text()',
#       'down': '/span[@class="down"]/text()',
#     }
#     for one in path:
#       p = response.xpath(one)
#       for k, v in clazz.items():
#         percent = util.String2Number(''.join(p.xpath(v).extract()).strip())
#         if not np.isnan(percent):
#           return (k, percent)
#
#
#
#   def parse(self, response):
#     self.received.add(response.url)
#
#     if 'step' not in response.meta or response.meta['step'] == 0:
#       districts = self.parseDistricts(response)
#       realOut = set(districts) - self.received
#       for one in realOut:
#         yield Request(one, meta={'step': 0})
#
#     if 'step' in response.meta and response.meta['step'] <= 1:
#       subDistricts = self.parseSubDistricts(response)
#       realOut = set(subDistricts) - self.received
#       for one in realOut:
#         yield Request(one, meta={'step': 1, 'url': one})
#
#     district = ''
#     subDistrict = ''
#
#     if 'step' in response.meta:
#
#       if response.meta['step'] == 1:
#         d = response.xpath(self.xpath['districtName']).extract()
#         if len(d):
#           district = d[0]
#
#         d = response.xpath(self.xpath['subDistrictName']).extract()
#         if len(d):
#           subDistrict = d[0]
#
#         number = util.String2Number(''.join(response.xpath(self.xpath['districtNumber']).extract()).strip())
#         n = items.HouseDetailDigest()
#         n['city'] = self.city
#         n['src'] = self.src
#         n['district'] = district
#         n['subDistrict'] = subDistrict
#         n['number'] = number
#         today = util.todayString()
#         try:
#           n['_id'] = today + '_' + self.city + '_' + district + '_' + subDistrict
#         except Exception as e:
#           print(e)
#         updown = self.parseUpDown(response)
#         if updown is not None:
#           n['updown'] = updown[0]
#           n['percent'] = updown[1]
#         yield n
#
#
#
#         nextPage = self.nextPage(response, self.head, response.meta['url'], number)
#         realOut = set(nextPage) - self.received
#         for one in realOut:
#           print('next url: %s %s %s' % (district, subDistrict, one))
#           yield Request(one, meta={'step': 2, 'district': district, 'subDistrict': subDistrict})
#
#       if response.meta['step'] == 2:
#         district = response.meta['district']
#         subDistrict = response.meta['subDistrict']
#
#       if response.meta['step'] >= 1:
#         ones = response.xpath(self.xpath['lists'])
#
#         for one in ones:
#           oneOut = self.parseOne(one, district, subDistrict)
#           yield oneOut