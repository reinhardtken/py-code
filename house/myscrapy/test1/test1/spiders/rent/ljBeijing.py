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
  name = 'lianjia-zf-bj'
  city = '北京'
  allowed_domains = [
    'bj.lianjia.com',
  ]
  start_urls = [
    'https://bj.lianjia.com/zufang/dongcheng/'
  ]
  head = 'https://bj.lianjia.com'
  nextPageOrder = -1
  reversed = False
  dbName = 'house-zf'
  collectionName = 'beijing'

  xpath = {
    'districts': '//*[@id="filter-options"]/dl[1]/dd/div[1]/a',
    'districtName': '//*[@id="filter-options"]/dl[1]/dd/div[1]/a[@class="on"]/text()',
    'subDistricts': '//*[@id="filter-options"]/dl[1]/dd/div[2]/a',
    'subDistrictName': '//*[@id="filter-options"]/dl[1]/dd/div[2]/a[@class="on"]/text()',


    'lists': '//*[@id="house-lst"]/li',

    'districtNumber': '/html/body/div[4]/div[3]/div[2]/div[1]/h2/span/text()',

    'nextPageText': '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/a[last()]/text()',
    'nextPage': '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/a[last()]/@href',
    'allPage': '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/a',
    'allPage2': '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/a[last()-1]/@href',

    # 'startAnchor': '/html/body/div[5]/div[1]/div[2]/div[1]/span/text()',
    'anchor': '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/a[last()]',
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
        np.extend(url + one.xpath('.//@href').extract())

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
    maxNumber = String2Number(tmp[-2]) if tmp[-1] == '' else String2Number(tmp[-1])
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
    oneOut = items.LianjiaRentHouseItem()
    oneOut['district'] = district
    oneOut['subDistrict'] = subDistrict
    oneOut['_id'] = ''.join(one.xpath('./@data-housecode').extract()).strip()
    oneOut['title'] = ''.join(one.xpath('./div[2]/h2/a/text()').extract()).strip()

    try:
      oneOut['community'] = ''.join(one.xpath('./div[2]/div[1]/div[1]/a/span/text()').extract()).strip()
      oneOut['houseType'] = ''.join(one.xpath('./div[2]/div[1]/div[1]/span[1]/span/text()').extract()).strip()
      oneOut['square'] = String2Number(''.join(one.xpath('./div[2]/div[1]/div[1]/span[2]/text()').extract()).strip())

      oneOut['rentPrice'] = String2Number(''.join(one.xpath('./div[2]/div[2]/div[1]/span/text()').extract()).strip())

      oneOut['level'] = ''.join(one.xpath('./div[2]/div[1]/div[2]/div/text()[1]').extract())
      oneOut['structure'] = ''.join(one.xpath('./div[2]/div[1]/div[2]/div/text()[2]').extract())

      release = ''.join(one.xpath('./div[2]/div[2]/div[2]/text()').extract()).strip()
      oneOut['release'] = datetime.datetime.strptime(release[:10], '%Y.%m.%d')
      oneOut['follow'] = String2Number(''.join(one.xpath('./div[2]/div[3]/div/div[1]/span/text()').extract()).strip())
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

        number = String2Number(''.join(response.xpath(self.xpath['districtNumber']).extract()).strip())
        n = items.LianjiaRentHouseDetailDigest()
        n['city'] = self.city
        n['district'] = district
        n['subDistrict'] = subDistrict
        n['number'] = number
        n['_id'] = todayString() + '_' + n['city'] + '_' + n['district'] + '_' + n['subDistrict']
        yield n

        nextPage = self.nextPage(response, self.head, response.meta['url'])
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
