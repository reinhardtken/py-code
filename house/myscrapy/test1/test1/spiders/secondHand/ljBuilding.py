# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime
import base64
import urllib

import scrapy
from scrapy.http import Request
import numpy as np


print("run lianjia-esf-building")
#########################################################
import sys
# sys.path.append(r'C:\workspace\code\self\github\py-code\house\')
#########################################################
import items
import util

#用来爬取具体小区的房子
class Spider(scrapy.Spider):
    name = 'lianjia-esf-building'
    city = '北京'
    src = 'lj'
    allowed_domains = [
      'bj.lianjia.com',
                       ]
    start_urls = [
      # 'https://bj.lianjia.com/ershoufang/rs龙泽苑西区/',
      'https://bj.lianjia.com/ershoufang/rs%E6%97%97%E8%83%9C%E5%AE%B6%E5%9B%AD/'
    ]
    head = 'https://bj.lianjia.com'
    # nextPageOrder = 1
    dbName = 'house-block'
    collectionName = 'beijing'
    xpath = {

      'name': '/html/body/div[4]/div[1]/div[5]/div/div[1]/div[1]/div/a[1]/text()',
      'block': '/html/body/div[4]/div[1]/div[5]/div/div[1]/div[1]/div/span/text()',
      'price': '/html/body/div[4]/div[1]/div[5]/div/div[1]/div[2]/div[1]/a/text()',
      'sellCounter': '/html/body/div[4]/div[1]/div[5]/div/div[1]/div[2]/div[2]/div[2]/text()',
      'traded': '/html/body/div[4]/div[1]/div[5]/div/div[1]/div[2]/div[3]/a/text()',
      'lookCounter': '/html/body/div[4]/div[1]/div[5]/div/div[1]/div[2]/div[4]/div[2]/text()',

        'lists': '/html/body/div[4]/div[1]/ul/li',

      'nextPageText': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()]/text()',
      'nextPage': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()]/@href',
      'allPage': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a',
      'allPage2': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()-1]/@href',

      'anchor': '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()]',
    }

    received = set()

    def parseBlock(self, response):
      oneOut = items.BlockItem()
      try:
        oneOut['name'] = util.ExtractString(response, self.xpath['name'])
        oneOut['block'] = util.ExtractString(response, self.xpath['block'])
        oneOut['price'] = util.ExtractNumber(response, self.xpath['price'])
        oneOut['sellCounter'] = util.ExtractNumber(response, self.xpath['sellCounter'])
        oneOut['traded'] = util.ExtractNumber(response, self.xpath['traded'])
        oneOut['lookCounter'] = util.ExtractNumber(response, self.xpath['lookCounter'])
      except Exception as e:
        print(e)
      oneOut['crawlDate'] = util.today()
      return oneOut


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
          #原始url 最后多一个/，导致无法匹配
          np.append(url + urllib.parse.quote(util.ExtractString(one, './/@href')) + '/')

      return np


    def nextPage(self, response, url1, url2):
      out = self.nextPagePlusOne(response, url1)
      # out2 = []
      # for one in out:
      #   #out2.append(str(base64.b64encode(one.encode('utf-8')), 'utf-8'))
      #   out2.append(urllib.parse.quote(one))

      return out


    def parseOne(self, one, block, housecode):
      oneOut = items.HouseItem2()
      oneOut['src'] = self.src

      try:
        #/html/body/div[3]/div/div/div[1]/h1
        oneOut['title'] = util.ExtractString(one, '/html/body/div[3]/div/div/div[1]/h1/text()')
        # 这个是链家编号+crawldate
        oneOut['_id'] = housecode#util.ExtractString(one, '/html/body/div[5]/div[2]/div[6]/div[4]/span[2]')
        # 这个是真实的链家编号
        oneOut['houseID'] = oneOut['_id']

        oneOut['_id'] += '_' + util.todayString()

        oneOut['unitPrice'] = util.ExtractNumber(one, '/html/body/div[5]/div[2]/div[4]/div[1]/div[1]/span')
        oneOut['totalPrice'] = util.ExtractNumber(one, '/html/body/div[5]/div[2]/div[4]/span[1]')

        oneOut['community'] = block
        oneOut['houseType'] = util.ExtractString(one, '/html/body/div[5]/div[2]/div[5]/div[1]/div[1]/text()')#
        oneOut['square'] = util.ExtractNumber(one, '/html/body/div[5]/div[2]/div[5]/div[3]/div[1]')

        oneOut['level'] = util.ExtractString(one, '/html/body/div[5]/div[2]/div[5]/div[1]/div[2]/text()')
        oneOut['structure'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[1]/text()')

        oneOut['thb'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[10]/text()')
        oneOut['lx'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[6]/text()')

        oneOut['heating'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[11]/text()')
        oneOut['property'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[13]/text()')

        oneOut['attention'] = util.ExtractNumber(one, '//*[@id="favCount"]')
        oneOut['follow'] = util.ExtractNumber(one, '//*[@id="cartCount"]')
        oneOut['release'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[1]/span[2]/text()')
        oneOut['lastTrade'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[3]/span[2]/text()')
        oneOut['years'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[5]/span[2]/text()')
        oneOut['mortgage'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()').strip()

        #/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[6]/span[2]
        oneOut['ownership'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[2]/span[2]/text()')
        oneOut['use'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[4]/span[2]/text()')
        oneOut['propertyRight'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[6]/span[2]/text()')
        oneOut['book'] = util.ExtractString(one, '/html/body/div[7]/div[1]/div[1]/div/div/div[2]/div[2]/ul/li[8]/span[2]/text()')

        oneOut['crawlDate'] = util.today()

      except Exception as e:
        print(e)
        logging.warning("parseOne Exception %s"%(str(e)))
      return oneOut




    def parse(self, response):
      self.received.add(response.url)

      # districts = self.parseDistricts(response)
      # realOut = set(districts) - self.received
      # for one in realOut:
      #   yield Request(one, meta={'step': 0})
      #
      # subDistricts = self.parseSubDistricts(response)
      # realOut = set(subDistricts) - self.received
      # for one in realOut:
      #   yield Request(one, meta={'step': 1, 'url': one})

      blockName = None
      if 'block' not in response.meta:
        #本小区摘要信息
        block = self.parseBlock(response)
        blockName = block['name']
        # yield block
        #所有同级页面
        nextPage = self.nextPage(response, self.head, None)
        realOut = set(nextPage) - self.received
        for one in realOut:
          #这个是一共多少页
          yield Request(one, meta={'step': 2, 'block': block['name']})
      else:
        blockName = response.meta['block']

      ones = response.xpath(self.xpath['lists'])
      for one in ones:
        # 这个是每页多少条
        try:
          url = util.ExtractString(one, './/div[1]/div[1]/a/@href')
          housecode = util.ExtractString(one, './/div[1]/div[1]/a/@data-housecode')
          yield Request(url, meta={'step': 3, 'block': blockName, 'hc': housecode})
        except Exception as e:
          print(e)


      if 'step' in response.meta and response.meta['step'] ==3:
        oneOut = self.parseOne(response, blockName, response.meta['hc'])
        if len(oneOut['_id']):
          yield oneOut
          
