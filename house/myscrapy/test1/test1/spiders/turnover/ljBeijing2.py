# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime
import datetime

import scrapy
from scrapy.http import Request
import numpy as np


import items
import util




class Spider(scrapy.Spider):
  name = 'lianjia-cj-bj'
  city = '北京'
  allowed_domains = [
    'bj.lianjia.com',
  ]
  start_urls = [
    'https://bj.lianjia.com/chengjiao/dongcheng/'
    # 'https://bj.lianjia.com/chengjiao/pinggu/'
  ]
  head = 'https://bj.lianjia.com'
  nextPageOrder = 1
  reversed = True
  dbName = 'house-cj'
  collectionName = 'beijing'
  #true时，增量crawl，否则全量crawl
  incrementMode = True

  xpath = {
    'districts': '/html/body/div[3]/div[1]/dl[2]/dd/div/div[1]/a',
    'districtName': '/html/body/div[3]/div[1]/dl[2]/dd/div/div[1]/a[@class="selected"]/text()',
    'subDistricts': '/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a',
    'subDistrictName': '/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a[@class="selected"]/text()',


    'lists': '/html/body/div[5]/div[1]/ul/li',

    'districtNumber': '/html/body/div[5]/div[1]/div[2]/div[1]/span/text()',

    'nextPageText': '/html/body/div[5]/div[1]/div[5]/div[2]/div/a[last()]/text()',
    'nextPage': '/html/body/div[5]/div[1]/div[5]/div[2]/div/a[last()]/@href',
    'allPage': '/html/body/div[5]/div[1]/div[5]/div[2]/div/a',
    'allPage2': '/html/body/div[5]/div[1]/div[5]/div[2]/div/a[last()-1]/@href',

    'startAnchor': '/html/body/div[5]/div[1]/div[2]/div[1]/span/text()',
    'anchor': '/html/body/div[5]/div[1]/div[5]/div[2]/div/a[last()]',
  }

  received = set()
  timeStampStop = util.today() - datetime.timedelta(weeks=8)
  stopMax= 30
  stopCounerMap = {}

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


  def parseSubDistricts(self, response):
    out = []
    ones = response.xpath(self.xpath['subDistricts'])
    for one in ones:
      urls = one.xpath('.//@href').extract()
      for url in urls:
        if url.startswith('http'):
          # out.append(url)
          pass
        else:
          out.append(self.head + url)

    return out


  def nextPagePlusOne(self, response, url):
    np = []
    nextPageText = ''.join(response.xpath(self.xpath['nextPageText']).extract()).strip()
    if nextPageText == '下一页':
      for one in response.xpath(self.xpath['nextPage']).extract():
        np.append(url + one)
    else:
      p = response.xpath(self.xpath['allPage'])
      # 框架支持url排重,这里就不排重了
      for one in p:
        k = one.xpath('.//@href').extract()
        if isinstance(k, list):
          np.append(url + k[0])
        else:
          np.append(url + k)

    return np

  def nextPageNegativeOne(self, response, url):
    np = []
    maxURL = None
    nextPageText = ''.join(response.xpath(self.xpath['nextPageText']).extract()).strip()
    if nextPageText == '下一页':
      tmp = response.xpath(self.xpath['allPage2']).extract()
      if len(tmp):
        maxURL = tmp[0].strip()
    else:
      tmp = response.xpath(self.xpath['nextPage']).extract()
      if len(tmp):
        maxURL = tmp[0].strip()

    if maxURL is None:
      return []

    tmp = maxURL.split('/')
    maxNumber = util.String2Number(tmp[-2]) if tmp[-1] == '' else util.String2Number(tmp[-1])
    if self.reversed:
      for i in range(int(maxNumber), 1, -1):
        np.append(url + 'pg' + str(i))
    else:
      for i in range(2, int(maxNumber) + 1):
        np.append(url + 'pg' + str(i))

    return np

  def nextPage(self, response, url1, url2):
    if self.nextPageOrder == -1:
      return self.nextPageNegativeOne(response, url2)
    else:
      return self.nextPagePlusOne(response, url1)


  def parseOne(self, one, district, subDistrict):
    oneOut = items.LianjiaTurnoverHouseItem()
    oneOut['district'] = district
    oneOut['subDistrict'] = subDistrict
    oneOut['title'] = ''.join(one.xpath('./div/div[1]/a/text()').extract()).strip()
    oneOut['href'] = ''.join(one.xpath('./div/div[1]/a/@href').extract()).strip()
    if len(oneOut['href']) > 0:
      id = '-1'
      try:
        id = oneOut['href'].split('/')[-1][:-5]
      except Exception as e:
        logging.warning("parseOne Exception %s" % (str(e)))
      oneOut['_id'] = id

    try:
      oneOut['askPrice'] = util.String2Number(''.join(one.xpath('./div/div[5]/span[2]/span[1]/text()').extract()).strip())
      oneOut['dealCycle'] = util.String2Number(''.join(one.xpath('./div/div[5]/span[2]/span[2]/text()').extract()).strip())
      if np.isnan(oneOut['askPrice']):
        #https://bj.lianjia.com/chengjiao/pinggu/
        oneOut['askPrice'] = util.String2Number(''.join(one.xpath('./div/div[4]/span[2]/span[1]/text()').extract()).strip())
        oneOut['dealCycle'] = util.String2Number(''.join(one.xpath('./div/div[4]/span[2]/span[2]/text()').extract()).strip())

      oneOut['bidPrice'] = util.String2Number(''.join(one.xpath('./div/div[2]/div[3]/span/text()').extract()).strip())
      oneOut['dealDate'] = ''.join(one.xpath('./div/div[2]/div[2]/text()').extract()).strip()

    except Exception as e:
      print(e)
      logging.warning("parseOne Exception %s" % (str(e)))
    return oneOut

  def parse(self, response):
    self.received.add(response.url)

    districts = self.parseDistricts(response)
    realOut = set(districts) - self.received
    for one in realOut:
      yield Request(one, meta={'step': 0})

    subDistricts = self.parseSubDistricts(response)
    realOut = set(subDistricts) - self.received
    for one in realOut:
      yield Request(one, meta={'step': 1, 'url': one})


    district = ''
    subDistrict = ''


    if 'step' in response.meta:

      if response.meta['step'] == 1:
        d = response.xpath(self.xpath['districtName']).extract()
        if len(d):
          district = d[0]

        d = response.xpath(self.xpath['subDistrictName']).extract()
        if len(d):
          subDistrict = d[0]

        number = util.String2Number(''.join(response.xpath(self.xpath['districtNumber']).extract()).strip())
        n = items.LianjiaTurnoverHouseDetailDigest()
        n['city'] = self.city
        n['district'] = district
        n['subDistrict'] = subDistrict
        n['number'] = number
        n['_id'] = util.todayString() + '_' + n['city'] + '_' + n['district'] + '_' + n['subDistrict']
        yield n


      if response.meta['step'] == 2:
        district = response.meta['district']
        subDistrict = response.meta['subDistrict']

      if response.meta['step'] >= 1:
        ones = response.xpath(self.xpath['lists'])

        for one in ones:
          oneOut = self.checkGoon(self.parseOne(one, district, subDistrict), response)
          if oneOut[0] == 0:
            continue
          elif oneOut[0] == -1:
            return None

          yield oneOut[1]


        if response.meta['step'] == 1:
          nextPage = self.nextPage(response, self.head, response.meta['url'])
          realOut = set(nextPage) - self.received
          for one in realOut:
            # nextURL = self.head + one
            print('next url: %s %s %s' % (district, subDistrict, one))
            yield Request(one, meta={'step': 2, 'url': response.meta['url'], 'district': district, 'subDistrict': subDistrict})

  #1 valid data,0,invalid data,-1 stop this district crawl
  def checkGoon(self, item, response):
    if np.isnan(item['bidPrice']) or item['bidPrice'] < 10:
      # 最近一个月成交，缺少具体数据
      return (0, )
    else:
      try:
        item['diffPricePercent'] = (item['askPrice'] - item['bidPrice']) / item['askPrice']
        item['dealDate'] = datetime.datetime.strptime(item['dealDate'], '%Y.%m.%d')

        title = item['title']
        tmp = title.strip().split(' ')
        item['building'] = None
        item['houseType'] = None
        item['square'] = None
        if len(tmp) > 0:
          item['building'] = tmp[0]
          if len(tmp) > 1:
            item['houseType'] = tmp[1]
            if len(tmp) > 2:
              item['square'] = util.String2Number(tmp[2])
              item['unitPrice'] = item['bidPrice'] / item['square']
      except Exception as e:
        logging.warning("processTurnoverData Exception %s" % (str(e)))

      if self.incrementMode and item['dealDate'] < self.timeStampStop:
        if response.meta['url'] in self.stopCounerMap:
          self.stopCounerMap[response.meta['url']] += 1
          if self.stopCounerMap[response.meta['url']] > self.stopMax:
            return (-1, )
        else:
          self.stopCounerMap[response.meta['url']] = 1
      else:
        pass

      return (1, item)