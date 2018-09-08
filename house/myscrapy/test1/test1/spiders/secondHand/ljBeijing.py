# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime

import scrapy
from scrapy.http import Request
import numpy as np


import items
import spiders.secondHand.ljShanghai

def String2Number(s):
  out = np.nan
  try:
    out = float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])
  except Exception as e:
    pass

  return out


# def todayString():
#   now = datetime.datetime.now()
#   now = now.replace(hour=0, minute=0, second=0, microsecond=0)
#   return now.strftime('%Y-%m-%d')


class Spider(spiders.secondHand.ljShanghai.Spider):
  name = 'lianjia-esf-bj'
  city = '北京'
  src = 'lj'
  allowed_domains = [
    'bj.lianjia.com',
  ]
  start_urls = [
    'https://bj.lianjia.com/ershoufang/chaoyang/',
  ]
  head = 'https://bj.lianjia.com'

  collectionName = 'beijing'

  xpath = {
    'districts': '//*[@id="position"]/dl[2]/dd/div[1]/div[1]/a',
    'districtName': '//*[@id="position"]/dl[2]/dd/div[1]/div[1]/a[@class="selected"]/text()',
    'subDistricts': '//*[@id="position"]/dl[2]/dd/div[1]/div[2]/a',
    'subDistrictName': '//*[@id="position"]/dl[2]/dd/div[1]/div[2]/a[@class="selected"]/text()',
    'districtNumber': '//*[@id="leftContent"]/div[1]/h2/span/text()',

     'lists': '//*[@id="leftContent"]/ul/li',

    'nextPageText': '//*[@id="leftContent"]/div[8]/div[2]/div/a[last()]/text()',
    'nextPage': '//*[@id="leftContent"]/div[8]/div[2]/div/a[last()]/@href',
    'allPage': '//*[@id="leftContent"]/div[8]/div[2]/div/a',
    'allPage2': '//*[@id="leftContent"]/div[8]/div[2]/div/a[last()-1]/@href',

    'anchor': '//*[@id="leftContent"]/div[8]/div[2]/div/a[last()]',
  }


  def parseOne(self, one, district, subDistrict):
    oneOut = items.HouseItem()
    oneOut['src'] = self.src
    oneOut['district'] = district
    oneOut['subDistrict'] = subDistrict
    oneOut['title'] = ''.join(one.xpath('./div/div[1]/a/text()').extract()).strip()
    oneOut['_id'] = ''.join(one.xpath('./div/div[1]/a/@data-housecode').extract()).strip()
    try:
      # oneOut['building'] = ''.join(one.xpath('.//div/div[2]/div/a/text()').extract()).strip()
      oneOut['unitPrice'] = String2Number(
        ''.join(one.xpath('./div/div[4]/div[3]/div[2]/span/text()').extract()).strip())
      oneOut['totalPrice'] = String2Number(
        ''.join(one.xpath('./div/div[4]/div[3]/div[1]/span/text()').extract()).strip())
      if np.isnan(oneOut['unitPrice']):
        oneOut['unitPrice'] = String2Number(
          ''.join(one.xpath('./div/div[4]/div[2]/div[2]/span/text()').extract()).strip())
        oneOut['totalPrice'] = String2Number(
          ''.join(one.xpath('./div/div[4]/div[2]/div[1]/span/text()').extract()).strip())

      oneOut['community'] = ''.join(one.xpath('./div/div[2]/div/a/text()').extract())
      oneOut['houseType'] = ''.join(one.xpath('./div/div[2]/div/text()[1]').extract())
      oneOut['square'] = String2Number(''.join(one.xpath('./div/div[2]/div/text()[2]').extract()))

      oneOut['level'] = ''.join(one.xpath('./div/div[3]/div/text()[1]').extract())
      if oneOut['level'][-1] == '万':
        oneOut['level'] = oneOut['level'][:-1]
      oneOut['structure'] = ''.join(one.xpath('./div/div[3]/div/text()[2]').extract())
      oneOut['area'] = ''.join(one.xpath('./div/div[3]/div/a/text()').extract())

      oneOut['attention'] = ''.join(one.xpath('./div/div[4]/text()[1]').extract())
      oneOut['follow'] = ''.join(one.xpath('./div/div[4]/text()[2]').extract())
      oneOut['release'] = ''.join(one.xpath('./div/div[4]/div[1]/text()').extract())

    except Exception as e:
      print(e)
      logging.warning("parseOne Exception %s"%(str(e)))
    return oneOut

