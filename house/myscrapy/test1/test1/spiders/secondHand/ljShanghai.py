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
    name = 'lianjia-esf-sh'
    city = '上海'
    src = 'lj'
    allowed_domains = [
      'sh.lianjia.com',
                       ]
    start_urls = [
      'https://sh.lianjia.com/ershoufang/pudong/',
    ]
    head = 'https://sh.lianjia.com'
    nextPageOrder = -1
    dbName = 'house'
    collectionName = 'shanghai'
    xpath = {
      'districts': '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[1]/a',
      'districtName': '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[1]/a[@class="selected"]/text()',
      'subDistricts': '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a',
      'subDistrictName': '/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a[@class="selected"]/text()',
      'districtNumber': '/html/body/div[4]/div[1]/div[2]/h2/span/text()',

        'lists': '/html/body/div[4]/div[1]/ul/li',

      'nextPageText': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()]/text()',
      'nextPage': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()]/@href',
      'allPage': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a',
      'allPage2': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()-1]/@href',

      'anchor': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()]',
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
          np.append(url + one.xpath('.//@href').extract())

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

      if maxURL is not None:
        tmp = maxURL.split('/')
        maxNumber = util.String2Number(tmp[-2]) if tmp[-1] == '' else util.String2Number(tmp[-1])
        for i in range(2, int(maxNumber) + 1):
          np.append(url + 'pg' + str(i))

      return np

    def nextPage(self, response, url1, url2):
      if self.nextPageOrder == -1:
        return self.nextPageNegativeOne(response, url2)
      else:
        return self.nextPagePlusOne(response, url1)


    def parseOne(self, one, district, subDistrict):
      oneOut = items.HouseItem()
      oneOut['src'] = self.src
      oneOut['district'] = district
      oneOut['subDistrict'] = subDistrict
      oneOut['title'] = ''.join(one.xpath('.//div[1]/div[1]/a/text()').extract()).strip()
      oneOut['_id'] = ''.join(one.xpath('.//div[1]/div[1]/a/@data-housecode').extract()).strip()
      try:
        unitPrice = util.String2Number(''.join(one.xpath('.//div[1]/div[6]/div[2]/span/text()').extract()).strip())
        if not np.isnan(unitPrice):
          oneOut['unitPrice'] = unitPrice
          oneOut['totalPrice'] = util.String2Number(
            ''.join(one.xpath('.//div[1]/div[6]/div[1]/span/text()').extract()).strip())
        else:
          #https://sh.lianjia.com/ershoufang/changning/pg96/
          oneOut['unitPrice'] = util.String2Number(''.join(one.xpath('.//div[1]/div[7]/div[2]/span/text()').extract()).strip())
          oneOut['totalPrice'] = util.String2Number(
            ''.join(one.xpath('.//div[1]/div[7]/div[1]/span/text()').extract()).strip())

        oneOut['community'] = ''.join(one.xpath('.//div[1]/div[2]/div/a/text()').extract())
        houseInfo = ''.join(one.xpath('.//div[1]/div[2]/div/text()').extract())
        houseInfo = houseInfo.split('|')
        if len(houseInfo) > 1:
          oneOut['houseType'] = houseInfo[1].strip()
          if len(houseInfo) > 2:
            oneOut['square'] = util.String2Number(houseInfo[2].strip())

        oneOut['area'] = ''.join(one.xpath('.//div[1]/div[3]/div/a/text()').extract())
        positionInfo = ''.join(one.xpath('.//div[1]/div[3]/div/text()').extract())
        positionInfo = positionInfo.split(')')
        if len(positionInfo) > 0:
          oneOut['level'] = positionInfo[0].strip() + ')'
          if len(positionInfo) > 1:
            oneOut['structure'] = positionInfo[1].strip()

        followInfo = ''.join(one.xpath('.//div[1]/div[4]/text()').extract())
        followInfo = followInfo.split('/')
        if len(followInfo) > 0:
          oneOut['attention'] = followInfo[0].strip()
          if len(followInfo) > 1:
            oneOut['follow'] = followInfo[1].strip()
            if len(followInfo) > 2:
              oneOut['release'] = followInfo[2].strip()

        oneOut['crawlDate'] = util.today()

      except Exception as e:
        print(e)
        logging.warning("parseOne Exception %s"%(str(e)))
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


      district = np.nan
      subDistrict = np.nan


      if 'step' in response.meta:

        if response.meta['step'] == 1:
          d = response.xpath(self.xpath['districtName']).extract()
          if len(d):
            district = d[0]

          d = response.xpath(self.xpath['subDistrictName']).extract()
          if len(d):
            subDistrict = d[0]

          number = util.String2Number(''.join(response.xpath(self.xpath['districtNumber']).extract()).strip())
          n = items.HouseDetailDigest()
          n['city'] = self.city
          n['src'] = self.src
          n['district'] = district
          n['subDistrict'] = subDistrict
          n['number'] = number
          n['_id'] = util.todayString() + '_' + n['city'] + '_' + n['district'] + '_' + n['subDistrict']
          yield n

          nextPage = self.nextPage(response, self.head, response.meta['url'])
          realOut = set(nextPage) - self.received
          for one in realOut:
            # nextURL = self.head + one
            print('next url: %s %s %s'%(district, subDistrict, one))
            yield Request(one, meta={'step': 2, 'district': district, 'subDistrict': subDistrict})

        if response.meta['step'] == 2:
          district = response.meta['district']
          subDistrict = response.meta['subDistrict']

        if response.meta['step'] >= 1:
          ones = response.xpath(self.xpath['lists'])

          for one in ones:
            oneOut = self.parseOne(one, district, subDistrict)
            if len(oneOut['_id']):
              yield oneOut
            else:
              continue
