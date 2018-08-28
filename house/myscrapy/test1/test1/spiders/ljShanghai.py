# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items

def String2Number(s):
  import re
  return float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])

class LJShanghaiSpider(scrapy.Spider):
    name = 'lianjia-sh'
    allowed_domains = [
      'sh.lianjia.com',
                       ]
    start_urls = [
      'https://sh.lianjia.com/ershoufang/pudong/',
    ]
    head = 'https://sh.lianjia.com'
    dbName = 'house'
    collectionName = 'shanghai'

    def parseDistricts(self, response):
      out = []

      ones = response.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[1]/a')
      for one in ones:
        urls = one.xpath('.//@href').extract()
        for url in urls:
          if url.startswith('http'):
            # out.append(url)
            pass
          else:
            out.append(self.head + url)

      return out


    def parse(self, response):
      districts = self.parseDistricts(response)
      for one in districts:
        yield Request(one)

      ones = response.xpath('/html/body/div[4]/div[1]/ul/li')

      district = 'nan'
      d = response.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[1]/a[@class="selected"]/text()').extract()
      if len(d):
        district = d[0]

      nextPage = []
      nextPageText = ''.join(response.xpath('/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()]/text()').extract()).strip()
      if nextPageText == '下一页':
        nextPage.extend(response.xpath('/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()]/@href').extract())
      else:
        p = response.xpath('/html/body/div[4]/div[1]/div[8]/div[2]/div/a')
        # 框架支持url排重,这里就不排重了
        for one in p:
          nextPage.extend(one.xpath('.//@href').extract())

      for one in nextPage:
        nextURL = self.head + one
        print('next url: %s'%(nextURL))
        yield Request(nextURL)

      for one in ones:
        oneOut = items.LianjiaHouseItem()
        oneOut['district'] = district
        oneOut['title'] = ''.join(one.xpath('.//div[1]/div[1]/a/text()').extract()).strip()
        oneOut['_id'] = ''.join(one.xpath('.//div[1]/div[1]/a/@data-housecode').extract()).strip()
        try:
          oneOut['unitPrice'] = String2Number(''.join(one.xpath('.//div[1]/div[6]/div[2]/span/text()').extract()).strip())
          oneOut['totalPrice'] = String2Number(''.join(one.xpath('.//div[1]/div[6]/div[1]/span/text()').extract()).strip())

          oneOut['community'] = ''.join(one.xpath('.//div[1]/div[2]/div/a/text()').extract())
          houseInfo = ''.join(one.xpath('.//div[1]/div[2]/div/text()').extract())
          houseInfo = houseInfo.split('|')
          if len(houseInfo) > 1:
            oneOut['houseType'] = houseInfo[1].strip()
            if len(houseInfo) > 2:
              oneOut['square'] = String2Number(houseInfo[2].strip())

          oneOut['area'] = ''.join(one.xpath('.//div[1]/div[3]/div/a/text()').extract())
          positionInfo = ''.join(one.xpath('.//div[1]/div[3]/div/text()').extract())
          positionInfo = positionInfo.split(')')
          if len(positionInfo) > 0:
            oneOut['level'] = positionInfo[0].strip() + ')'
            if len(houseInfo) > 1:
              oneOut['structure'] = positionInfo[1].strip()

          followInfo = ''.join(one.xpath('.//div[1]/div[4]/text()').extract())
          followInfo = followInfo.split('/')
          if len(followInfo) > 0:
            oneOut['attention'] = followInfo[0].strip()
            if len(houseInfo) > 1:
              oneOut['follow'] = followInfo[1].strip()
              if len(houseInfo) > 2:
                oneOut['release'] = followInfo[2].strip()

        except Exception as e:
          print(e)
        yield oneOut
