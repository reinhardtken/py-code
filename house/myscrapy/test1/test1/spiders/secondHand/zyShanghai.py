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
    name = 'zy-esf-sh'
    city = '上海'
    src = 'zy'
    allowed_domains = [
      'sh.centanet.com',
                       ]
    start_urls = [
      'https://sh.centanet.com/ershoufang/pudongxinqu/',
    ]
    head = 'https://sh.centanet.com'

    nextPageOrder = -1
    reversed = False
    useAllPge = True
    dbName = 'house'
    collectionName = 'shanghai'
    xpath = {

      'districts': '//*[@id="esfList"]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/ul[1]/li/a',
      'districtName': '//*[@id="esfList"]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/ul[1]/li[@class="tap_bg"]/text()',
      'subDistricts': '//*[@id="esfList"]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/ul/li/a',
      'subDistrictName': '//*[@id="esfList"]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/ul/li[@class="tap_bg"]/text()',
      'districtNumber': '//*[@id="esfList"]/div[3]/div/div[3]/h3/span/text()',

        'lists': '//*[@id="ShowStyleByTable"]/li',

      'nextPageText': '//*[@id="esfList"]/div[4]/div[2]/div/div/div/div[last()]/a/text()',
      'nextPage': '//*[@id="esfList"]/div[4]/div[2]/div/div/div/div[last()]/a/@href',
      'nextPageText2': '//*[@id="esfList"]/div[4]/div[2]/div/div/div/div[last()]/text()',
      'nextPage2': '//*[@id="esfList"]/div[4]/div[2]/div/div/div/div[last()]/@href',
      'allPage': '/html/body/div[3]/div[4]/div[2]/div/div/div/div[2]/ul/li[last()]/a/@href',
      # 'allPage2': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()-1]/@href',

      'anchor': '//*[@id="esfList"]/div[4]/div[2]/div/div/div/div[last()]/a',
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
            # if url.endswith('/0'):
            #   url = url[:-1]
            out.append(self.head + url)

      return out

    def nextPagePlusOne(self, response, url):
      #没有跑过
      np = []
      nextPageText = ''.join(response.xpath(self.xpath['nextPageText']).extract()).strip()
      if nextPageText == '下一页':
        for one in response.xpath(self.xpath['nextPage']).extract():
          np.append(url + one)
      else:
        nextPageText = ''.join(response.xpath(self.xpath['nextPageText2']).extract()).strip()
        if nextPageText == '下一页':
          for one in response.xpath(self.xpath['nextPage2']).extract():
            np.append(url + one)

      return np

    def nextPageNegativeOne(self, response, url, number):
      if self.useAllPge:
        return self.nextPageNegativeOneAllPage(response, url)
      else:
        return self.nextPageNegativeOneNumber(response, url, number)

    def nextPageNegativeOneNumber(self, response, url, number):
      out = []
      if not np.isnan(number):
        maxNumber = int(number / 20) + 1
        if self.reversed:
          for i in range(maxNumber, 1, -1):
            out.append(url + 'g' + str(i))
        else:
          for i in range(2, maxNumber + 1):
            one = url + 'g' + str(i)
            out.append(one)

      return out


    def nextPageNegativeOneAllPage(self, response, url):
      np = []
      maxURL = ''
      nextPageText = ''.join(response.xpath(self.xpath['nextPageText']).extract()).strip()
      if nextPageText == '下一页':
        a = response.xpath(self.xpath['allPage']).extract()
        for one in a:
          maxURL = one
          break
      else:
        nextPageText = ''.join(response.xpath(self.xpath['nextPageText2']).extract()).strip()
        if nextPageText == '下一页':
          a = response.xpath(self.xpath['allPage']).extract()
          for one in a:
            maxURL = one
            break

      if maxURL is '':
        return []

      tmp = maxURL.split('/')
      maxNumber = util.String2Number(tmp[-2]) if tmp[-1] == '' else util.String2Number(tmp[-1])
      if self.reversed:
        for i in range(int(maxNumber), 1, -1):
          np.append(url + 'g' + str(i))
      else:
        for i in range(2, int(maxNumber) + 1):
          np.append(url + 'g' + str(i))


      return np


    def nextPage(self, response, url1, url2, number):
      if self.nextPageOrder == -1:
        return self.nextPageNegativeOne(response, url2, number)
      else:
        return self.nextPagePlusOne(response, url1)


    def parseOne(self, one, district, subDistrict):
      oneOut = items.HouseItem()
      oneOut['src'] = self.src
      oneOut['district'] = district
      oneOut['subDistrict'] = subDistrict
      oneOut['title'] = ''.join(one.xpath('./div/div[2]/div[1]/a/text()').extract()).strip()
      href = ''.join(one.xpath('./div/div[2]/div[1]/a/@href').extract()).strip()
      if len(href) > 0:
        id = '-1'
        try:
          id = href.split('/')[-1][:-5]
        except Exception as e:
          logging.warning("parseOne Exception %s" % (str(e)))
        oneOut['_id'] = id

      try:
        totalPrice = util.String2Number(''.join(one.xpath('./div/div[3]/h3/span/text()').extract()).strip())
        oneOut['totalPrice'] = totalPrice
        oneOut['unitPrice'] = util.String2Number(
          ''.join(one.xpath('./div/div[3]/p/text()').extract()).strip())

        oneOut['community'] = ''.join(one.xpath('./div/div[2]/div[2]/a/text()').extract())

        tmp = ''.join(one.xpath('./div/div[2]/div[2]/text()').extract()).strip()
        tmp2 = tmp.split('|')
        if len(tmp2) > 0:
          oneOut['houseType'] = tmp2[0]
          if len(tmp2) > 1:
            oneOut['square'] = util.String2Number(tmp2[1])
            if len(tmp2) > 4:
              oneOut['level'] = tmp2[3] + '-' + tmp2[4]

        oneOut['crawlDate'] = util.today()

      except Exception as e:
        print(e)
        logging.warning("parseOne Exception %s"%(str(e)))
      return oneOut

    def parse(self, response):
      self.received.add(response.url)

      if 'step' not in response.meta or response.meta['step'] == 0:
        districts = self.parseDistricts(response)
        realOut = set(districts) - self.received
        for one in realOut:
          yield Request(one, meta={'step': 0})

      if 'step' in response.meta and response.meta['step'] <= 1:
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
          n = items.HouseDetailDigest()
          n['city'] = self.city
          n['src'] = self.src
          n['district'] = district
          n['subDistrict'] = subDistrict
          n['number'] = number
          today = util.todayString()
          try:
            n['_id'] = today + '_' + self.city + '_' + district + '_' + subDistrict
          except Exception as e:
            print(e)
          yield n

          nextPage = self.nextPage(response, self.head, response.meta['url'], number)
          realOut = set(nextPage) - self.received
          for one in realOut:
            print('next url: %s %s %s'%(district, subDistrict, one))
            yield Request(one, meta={'step': 2, 'district': district, 'subDistrict': subDistrict})

        if response.meta['step'] == 2:
          district = response.meta['district']
          subDistrict = response.meta['subDistrict']

        if response.meta['step'] >= 1:
          ones = response.xpath(self.xpath['lists'])

          for one in ones:
            oneOut = self.parseOne(one, district, subDistrict)
            yield oneOut
