# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime

import scrapy
from scrapy.http import Request
import numpy as np


import items


def String2Number(s):
  out = np.nan
  try:
    out = float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])
  except Exception as e:
    pass

  return out


def todayString():
  now = datetime.datetime.now()
  now = now.replace(hour=0, minute=0, second=0, microsecond=0)
  return now.strftime('%Y-%m-%d')


class Spider(scrapy.Spider):
    name = 'wiwj-esf-bj'
    city = '北京'
    src = 'wiwj'
    allowed_domains = [
      'bj.5i5j.com',
                       ]
    start_urls = [
      'https://bj.5i5j.com/ershoufang/chaoyangqu/',
    ]
    head = 'https://bj.5i5j.com'

    nextPageOrder = -1
    reversed = False
    dbName = 'house'
    collectionName = 'beijing'
    xpath = {
      'districts': '/html/body/div[3]/div[2]/div/ul/li[1]/div[3]/div[1]/ul/a',
      'districtName': '/html/body/div[3]/div[2]/div/ul/li[1]/div[3]/div[1]/ul/a/li[@class="new_di_tab_cur"]/text()',
      'subDistricts': '/html/body/div[3]/div[2]/div/ul/li[1]/div[3]/div[1]/dl/dd/a',
      'subDistrictName': '/html/body/div[3]/div[2]/div/ul/li[1]/div[3]/div[1]/dl/dd/a[@class="hover"]/text()',
      'districtNumber': '/html/body/div[4]/div[1]/div[1]/span/text()',

        'lists': '/html/body/div[4]/div[1]/div[2]/ul/li',

      'nextPageText': '/html/body/div[4]/div[1]/div[3]/div[2]/a[1]/text()',
      'nextPage': '/html/body/div[4]/div[1]/div[3]/div[2]/a[1]/@href',
      # 'allPage': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a',
      # 'allPage2': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()-1]/@href',

      'anchor': '/html/body/div[4]/div[1]/div[3]/div[2]/a[1]',
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
      np = []
      nextPageText = ''.join(response.xpath(self.xpath['nextPageText']).extract()).strip()
      if nextPageText == '下一页':
        for one in response.xpath(self.xpath['nextPage']).extract():
          np.append(url + one)
      # else:
      #   p = response.xpath(self.xpath['allPage'])
      #   # 框架支持url排重,这里就不排重了
      #   for one in p:
      #     np.extend(url + one.xpath('.//@href').extract())

      return np

    def nextPageNegativeOne(self, response, url, number):
      out = []
      if not np.isnan(number):
        maxNumber = int(number / 30) + 1
        if self.reversed:
          for i in range(maxNumber, 1, -1):
            out.append(url + 'n' + str(i))
        else:
          for i in range(2, maxNumber + 1):
            one = url + 'n' + str(i)
            out.append(one)

      return out


    def nextPage(self, response, url1, url2, number):
      if self.nextPageOrder == -1 and not np.isnan(number):
        return self.nextPageNegativeOne(response, url2, number)
      else:
        return self.nextPagePlusOne(response, url1)


    def parseOne(self, one, district, subDistrict):
      oneOut = items.HouseItem()
      oneOut['src'] = self.src
      oneOut['district'] = district
      oneOut['subDistrict'] = subDistrict
      oneOut['title'] = ''.join(one.xpath('./div[2]/h3/a/text()').extract()).strip()
      href = ''.join(one.xpath('./div[2]/h3/a/@href').extract()).strip()
      if len(href) > 0:
        id = '-1'
        try:
          id = href.split('/')[-1][:-5]
        except Exception as e:
          logging.warning("parseOne Exception %s" % (str(e)))
        oneOut['_id'] = id

      try:
        totalPrice = String2Number(''.join(one.xpath('./div[2]/div[1]/div/p[1]/strong/text()').extract()).strip())
        oneOut['totalPrice'] = totalPrice
        oneOut['unitPrice'] = String2Number(
          ''.join(one.xpath('./div[2]/div[1]/div/p[2]/text()').extract()).strip())

        community = ''.join(one.xpath('./div[2]/div[1]/p[2]/a/text()').extract())
        community = community.split(' ')
        if len(community) >= 2:
          oneOut['community'] = community[1]

        houseInfo = ''.join(one.xpath('./div[2]/div[1]/p[1]/text()').extract())
        houseInfo = houseInfo.split('·')
        if len(houseInfo) >= 1:
          oneOut['houseType'] = houseInfo[0].strip()
          if len(houseInfo) >= 2:
            oneOut['square'] = String2Number(houseInfo[1].strip())
            if len(houseInfo) >= 4:
              oneOut['level'] = houseInfo[3].strip()

        followInfo = ''.join(one.xpath('./div[2]/div[1]/p[3]/text()').extract())
        followInfo = followInfo.split('·')
        if len(followInfo) > 0:
          oneOut['attention'] = followInfo[0].strip()
          if len(followInfo) > 1:
            oneOut['follow'] = followInfo[1].strip()
            if len(followInfo) > 2:
              release = followInfo[2].strip()
              oneOut['release'] = datetime.datetime.strptime(release[:10], '%Y-%m-%d')

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

          number = String2Number(''.join(response.xpath(self.xpath['districtNumber']).extract()).strip())
          n = items.HouseDetailDigest()
          n['city'] = self.city
          n['src'] = self.src
          n['district'] = district
          n['subDistrict'] = subDistrict
          n['number'] = number
          n['_id'] = todayString() + '_' + n['city'] + '_' + n['district'] + '_' + n['subDistrict']
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
