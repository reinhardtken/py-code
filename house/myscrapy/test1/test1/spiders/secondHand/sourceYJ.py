# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime

import scrapy
from scrapy.http import Request
import numpy as np


import items



class SourceYJ(object):
    # name = 'yj-esf-sh'
    city = '上海'
    src = 'yj'
    allowed_domains = [
      'yijufangyou1.anjuke.com',
                       ]
    start_urls = [
      'https://yijufangyou1.anjuke.com/gongsi-esf/',
    ]
    head = 'https://yijufangyou1.anjuke.com'

    nextPageOrder = 1
    # reversed = False
    # useAllPge = True

    collectionName = 'shanghai'
    xpath = {
      # 'districts': '/html/body/div[4]/div/div[1]/div[1]/p[2]/a',
      # 'districtName': '/html/body/div[4]/div/div[1]/div[1]/p[2]/span[@class="curr"]/text()',
      # 'subDistricts': '/html/body/div[4]/div/div[1]/div[1]/p[3]/span/a',
      # 'subDistrictName': '/html/body/div[4]/div/div[1]/div[1]/p[3]/span[@class="curr"]/text()',
      # 'districtNumber': '/html/body/div[5]/div/div/p/span/span/text()',
                 '//*[@id="list"]/a[120]/dl/dt'
        'lists': '/html/body/div[4]/div[3]/div[1]/ul/li',
      'nextPageText': '/html/body/div[4]/div[3]/div[1]/div[2]/a[last()]/text()',
      'nextPage': '/html/body/div[4]/div[3]/div[1]/div[2]/a[last()]/@href',
      # 'allPage': '/html/body/div[7]/div/div/div/a[last()]/@href',
      # 'allPage2': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()-1]/@href',

      'anchor': '/html/body/div[4]/div[3]/div[1]/div[2]/a[last()]',
    }

    received = set()

    def nextPagePlusOne(self, response, url):
      np = []
      nextPageText = ''.join(response.xpath(self.xpath['nextPageText']).extract()).strip()
      if nextPageText == '下一页 >':
        for one in response.xpath(self.xpath['nextPage']).extract():
          np.append(url + one)
          break

      return np



    def nextPage(self, response):
      if self.nextPageOrder == 1:
        return self.nextPagePlusOne(response, response.url)
      else:
        return []


    def parseOne(self, one):
      oneOut = items.HouseItem()
      oneOut['src'] = self.src

      oneOut['title'] = ''.join(one.xpath('./div[2]/div[1]/a/text()').extract()).strip()
      href = ''.join(one.xpath('./div[2]/div[1]/a/@href').extract()).strip()
      if len(href) > 0:
        id = '-1'
        try:
          id = href.split('?')[0].split('/')[-1][:-5]
        except Exception as e:
          logging.warning("parseOne Exception %s" % (str(e)))
        oneOut['_id'] = id

      try:
        tmp = ''.join(one.xpath('./div[2]/div[3]/span/text()').extract()).strip()
        tmp = tmp.split(' ')
        if len(tmp) > 0:
          oneOut['community'] = tmp[0]
          if len(tmp) > 1:
            tmp2 = tmp.split('-')
            if len(tmp2) > 0:
              oneOut['district'] = tmp2[0]
              if len(tmp2) > 1:
                oneOut['subDistrict'] = tmp2[1]

        totalPrice = String2Number(''.join(one.xpath('./div[3]/span[1]/strong/text()').extract()).strip())
        oneOut['totalPrice'] = totalPrice
        oneOut['unitPrice'] = String2Number(
          ''.join(one.xpath('./div[3]/span[2]/text()').extract()).strip())

        oneOut['houseType'] = ''.join(one.xpath('./div[2]/div[2]/span[1]/text()').extract()).strip()
        oneOut['square'] = String2Number(''.join(one.xpath('./div[2]/div[2]/span[2]/text()').extract()).strip())
        oneOut['level'] = ''.join(one.xpath('./div[2]/div[2]/span[3]/text()').extract()).strip()
        oneOut['structure'] = ''.join(one.xpath('./div[2]/div[2]/span[4]/text()').extract()).strip()

        oneOut['crawlDate'] = today()

      except Exception as e:
        print(e)
        logging.warning("parseOne Exception %s"%(str(e)))
      return oneOut


    def anchor(self):
      return self.xpath['anchor']

    def parse(self, response):
      self.received.add(response.url)
      content = response.body
      data = content.decode('utf-8')

      nextPage = self.nextPage(response)
      realOut = set(nextPage) - self.received
      for one in realOut:
        # print('next url: %s %s %s' % (district, subDistrict, one))
        yield Request(one, callback=self.parse)


      ones = response.xpath(self.xpath['lists'])
      for one in ones:
        oneOut = self.parseOne(one)
        yield oneOut


