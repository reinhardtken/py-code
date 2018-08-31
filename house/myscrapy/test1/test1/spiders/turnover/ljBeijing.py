# -*- coding: utf-8 -*-
import urllib
import logging
import re

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


class Spider(scrapy.Spider):
  name = 'lianjia-cj-bj-old'
  allowed_domains = [
    'bj.lianjia.com',
  ]
  start_urls = [
    'https://bj.lianjia.com/chengjiao/dongcheng/'
    #'https://bj.lianjia.com/chengjiao/pinggu/'
  ]
  head = 'https://bj.lianjia.com'
  dbName = 'house-cj'
  collectionName = 'beijing'

  xpath = {
    'districts': '/html/body/div[3]/div[1]/dl[2]/dd/div/div[1]/a',
    'districtName': '/html/body/div[3]/div[1]/dl[2]/dd/div/div[1]/a[@class="selected"]/text()',

    'lists': '/html/body/div[5]/div[1]/ul/li',

    'nextPageText': '/html/body/div[5]/div[1]/div[5]/div[2]/div/a[last()]/text()',
    'nextPage': '/html/body/div[5]/div[1]/div[5]/div[2]/div/a[last()]/@href',
    'allPage': '/html/body/div[5]/div[1]/div[5]/div[2]/div/a',
  }

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

  def nextPage(self, response):
    np = []
    nextPageText = ''.join(response.xpath(self.xpath['nextPageText']).extract()).strip()
    if nextPageText == '下一页':
      np.extend(response.xpath(self.xpath['nextPage']).extract())
    else:
      p = response.xpath(self.xpath['allPage'])
      # 框架支持url排重,这里就不排重了
      for one in p:
        np.extend(one.xpath('.//@href').extract())

    if len(np) == 0:
      pass
    return np

  def parseOne(self, one, district):
    oneOut = items.LianjiaTurnoverHouseItem()
    oneOut['district'] = district
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
      oneOut['askPrice'] = String2Number(''.join(one.xpath('./div/div[5]/span[2]/span[1]/text()').extract()).strip())
      oneOut['dealCycle'] = String2Number(''.join(one.xpath('./div/div[5]/span[2]/span[2]/text()').extract()).strip())
      if np.isnan(oneOut['askPrice']):
        #https://bj.lianjia.com/chengjiao/pinggu/
        oneOut['askPrice'] = String2Number(''.join(one.xpath('./div/div[4]/span[2]/span[1]/text()').extract()).strip())
        oneOut['dealCycle'] = String2Number(''.join(one.xpath('./div/div[4]/span[2]/span[2]/text()').extract()).strip())

      oneOut['bidPrice'] = String2Number(''.join(one.xpath('./div/div[2]/div[3]/span/text()').extract()).strip())
      oneOut['dealDate'] = ''.join(one.xpath('./div/div[2]/div[2]/text()').extract()).strip()

    except Exception as e:
      print(e)
      logging.warning("parseOne Exception %s" % (str(e)))
    return oneOut

  def parse(self, response):
    districts = self.parseDistricts(response)
    for one in districts:
      yield Request(one)

    nextPage = self.nextPage(response)
    for one in nextPage:
      nextURL = self.head + one
      print('next url: %s' % (nextURL))
      yield Request(nextURL)

    ones = response.xpath(self.xpath['lists'])
    district = 'nan'
    d = response.xpath(self.xpath['districtName']).extract()
    if len(d):
      district = d[0]

    for one in ones:
      oneOut = self.parseOne(one, district)
      yield oneOut
