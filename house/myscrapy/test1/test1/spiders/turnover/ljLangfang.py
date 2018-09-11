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
import spiders.turnover.ljBeijing2



class Spider(spiders.turnover.ljBeijing2.Spider):
  name = 'lianjia-cj-lf'
  city = '廊坊'
  allowed_domains = [
    'lf.lianjia.com',
  ]
  start_urls = [
    'https://lf.lianjia.com/chengjiao/fuchengwuqigongjiaozongzhan/',
    'https://lf.lianjia.com/chengjiao/fuchengsiqi/',
    'https://lf.lianjia.com/chengjiao/shouertiancheng/',
    'https://lf.lianjia.com/chengjiao/tianyangcheng/',
    'https://lf.lianjia.com/chengjiao/tianyangcheng4dai/',
    'https://lf.lianjia.com/chengjiao/yanshunluguodao/',
    'https://lf.lianjia.com/chengjiao/yanjinghangcheng/',
    'https://lf.lianjia.com/chengjiao/yanshunluxi/',
    'https://lf.lianjia.com/chengjiao/yanshunludong/',
  ]
  head = 'https://lf.lianjia.com'
  nextPageOrder = -1
  incrementMode = False

  collectionName = 'langfang'

  url2DistrictMap = {
    'https://lf.lianjia.com/chengjiao/fuchengwuqigongjiaozongzhan/': '福成五期公交总站',
    'https://lf.lianjia.com/chengjiao/fuchengsiqi/': '福成四期',
    'https://lf.lianjia.com/chengjiao/shouertiancheng/': '首尔甜城',
    'https://lf.lianjia.com/chengjiao/tianyangcheng/': '天洋城',
    'https://lf.lianjia.com/chengjiao/tianyangcheng4dai/': '天洋城4代',
    'https://lf.lianjia.com/chengjiao/yanshunluguodao/': '燕顺路国道',
    'https://lf.lianjia.com/chengjiao/yanjinghangcheng/': '燕京航城',
    'https://lf.lianjia.com/chengjiao/yanshunluxi/': '燕顺路西',
    'https://lf.lianjia.com/chengjiao/yanshunludong/': '燕顺路东',
  }



  def parse(self, response):
    self.received.add(response.url)


    district = self.city
    subDistrict = ''
    if 'step' not in response.meta:
      subDistrict = self.url2DistrictMap[response.url]
    else:
      subDistrict = response.meta['subDistrict']

    ones = response.xpath(self.xpath['lists'])
    for one in ones:
      oneOut = self.checkGoon(self.parseOne(one, district, subDistrict), response)
      if oneOut[0] == 0:
        continue
      elif oneOut[0] == -1:
        return None

      yield oneOut[1]

    if 'step' not in response.meta:
      nextPage = self.nextPage(response, self.head, response.url)
      realOut = set(nextPage) - self.received
      for one in realOut:
        # nextURL = self.head + one
        print('next url: %s %s %s' % (district, subDistrict, one))
        yield Request(one,
                      meta={'step': 2, 'url': response.url, 'district': district, 'subDistrict': subDistrict})


