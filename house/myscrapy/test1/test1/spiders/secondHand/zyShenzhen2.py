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
    name = 'zy-esf-sz'
    city = '深圳'
    src = 'zy'
    allowed_domains = [
      'sz.centanet.com',
                       ]
    start_urls = [
      'https://sz.centanet.com/ershoufang/',
    ]
    head = 'https://sz.centanet.com'

    nextPageOrder = -1
    reversed = False
    useAllPge = True
    dbName = 'house'
    collectionName = 'shenzhen'
    xpath = {
      # 'districts': '/html/body/div[4]/div/div[1]/div[1]/p[2]/a',
      # 'districtName': '/html/body/div[4]/div/div[1]/div[1]/p[2]/span[@class="curr"]/text()',
      # 'subDistricts': '/html/body/div[4]/div/div[1]/div[1]/p[3]/span/a',
      # 'subDistrictName': '/html/body/div[4]/div/div[1]/div[1]/p[3]/span[@class="curr"]/text()',
      'districtNumber': '/html/body/div[5]/div/div/p/span/span/text()',

        'lists': '/html/body/div[6]/div/div',

      'nextPageText': '/html/body/div[7]/div/div/div/a[last()-1]/text()',
      'nextPage': '/html/body/div[7]/div/div/div/a[last()-1]/@href',
      'allPage': '/html/body/div[7]/div/div/div/a[last()]/@href',
      # 'allPage2': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()-1]/@href',

      'anchor': '/html/body/div[7]/div/div/div/a[last()-1]',
    }

    received = set()

    # def parseDistricts(self, response):
    #   out = []
    #
    #   ones = response.xpath(self.xpath['districts'])
    #   for one in ones:
    #     urls = one.xpath('.//@href').extract()
    #     for url in urls:
    #       if url.startswith('http'):
    #         # out.append(url)
    #         pass
    #       else:
    #         out.append(self.head + url)
    #
    #   return out
    #
    #
    # def parseSubDistricts(self, response):
    #   out = []
    #
    #   ones = response.xpath(self.xpath['subDistricts'])
    #   for one in ones:
    #     urls = one.xpath('.//@href').extract()
    #     for url in urls:
    #       if url.startswith('http'):
    #         # out.append(url)
    #         pass
    #       else:
    #         # if url.endswith('/0'):
    #         #   url = url[:-1]
    #         out.append(self.head + url)
    #
    #   return out

    def nextPagePlusOne(self, response, url):
      np = []
      nextPageText = ''.join(response.xpath(self.xpath['nextPageText']).extract()).strip()
      if nextPageText == '>':
        for one in response.xpath(self.xpath['nextPage']).extract():
          np.append(url + one)
      # else:
      #   p = response.xpath(self.xpath['allPage'])
      #   # 框架支持url排重,这里就不排重了
      #   for one in p:
      #     np.extend(url + one.xpath('.//@href').extract())

      return np

    def nextPageNegativeOne(self, response, url):
      if self.useAllPge:
        return self.nextPageNegativeOneAllPage(response, url)
      else:
        pass

    def nextPageNegativeOneNumber(self, response, url, number):
      out = []
      if not np.isnan(number):
        maxNumber = int(number / 25) + 1
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
      maxURL = None
      maxURL = ''.join(response.xpath(self.xpath['allPage']).extract()).strip()
      # if len(allPage):
      #   maxURL = allPage[0].strip()

      if maxURL is '':
        return []

      tmp = maxURL.split('/')
      maxNumber = String2Number(tmp[-2]) if tmp[-1] == '' else String2Number(tmp[-1])
      if self.reversed:
        for i in range(int(maxNumber), 1, -1):
          np.append(url + 'g' + str(i))
      else:
        for i in range(2, int(maxNumber) + 1):
          np.append(url + 'g' + str(i))

      return np


    def nextPage(self, response):
      if self.nextPageOrder == -1:
        return self.nextPageNegativeOne(response, response.url)
      else:
        pass


    def parseOne(self, one):
      oneOut = items.HouseItem()
      oneOut['src'] = self.src
      oneOut['district'] = ''.join(one.xpath('./div[1]/p[3]/a[1]/text()').extract()).strip()
      oneOut['subDistrict'] = ''.join(one.xpath('./div[1]/p[3]/a[2]/text()').extract()).strip()
      oneOut['title'] = ''.join(one.xpath('./div[1]/h4/a/text()').extract()).strip()
      href = ''.join(one.xpath('./div[1]/h4/a/@href').extract()).strip()
      if len(href) > 0:
        id = '-1'
        try:
          id = href.split('/')[-1][:-5]
        except Exception as e:
          logging.warning("parseOne Exception %s" % (str(e)))
        oneOut['_id'] = id

      try:
        totalPrice = String2Number(''.join(one.xpath('./div[2]/p[1]/span/text()').extract()).strip())
        oneOut['totalPrice'] = totalPrice
        oneOut['unitPrice'] = String2Number(
          ''.join(one.xpath('./div[2]/p[2]/text()').extract()).strip())

        oneOut['community'] = ''.join(one.xpath('./div[1]/p[1]/a/text()').extract())
        # community = community.split(' ')
        # if len(community) >= 2:
        #   oneOut['community'] = community[1]

        oneOut['houseType'] = ''.join(one.xpath('./div[1]/p[1]/span[2]/text()').extract()).strip()
        if oneOut['houseType'] == '|':
          oneOut['houseType'] = ''.join(one.xpath('./div[1]/p[1]/span[3]/text()').extract()).strip()

        oneOut['square'] = String2Number(''.join(one.xpath('./div[1]/p[1]/span[4]/text()').extract()).strip())
        if np.isnan(oneOut['square']):
          oneOut['square'] = String2Number(''.join(one.xpath('./div[1]/p[1]/span[5]/text()').extract()).strip())

        oneOut['level'] = ''.join(one.xpath('./div[1]/p[2]/span[1]/text()').extract()).strip()

        oneOut['crawlDate'] = today()

      except Exception as e:
        print(e)
        logging.warning("parseOne Exception %s"%(str(e)))
      return oneOut

    def parse(self, response):
      self.received.add(response.url)

      # if 'step' not in response.meta or response.meta['step'] == 0:
      #   districts = self.parseDistricts(response)
      #   realOut = set(districts) - self.received
      #   for one in realOut:
      #     yield Request(one, meta={'step': 0})

      # if 'step' in response.meta and response.meta['step'] <= 1:
      #   subDistricts = self.parseSubDistricts(response)
      #   realOut = set(subDistricts) - self.received
      #   for one in realOut:
      #     yield Request(one, meta={'step': 1, 'url': one})


      # district = ''
      # subDistrict = ''
      if 'step' not in response.meta:
        nextPage = self.nextPage(response)
        realOut = set(nextPage) - self.received
        for one in realOut:
          # print('next url: %s %s %s' % (district, subDistrict, one))
          yield Request(one, meta={'step': 2, })

      ones = response.xpath(self.xpath['lists'])
      for one in ones:
        oneOut = self.parseOne(one)
        yield oneOut


