# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items

def String2Number(s):
  import re
  return float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])

class BasicSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = [
      'bj.lianjia.com',
      'lf.lianjia.com',
                       ]
    start_urls = [
      'https://bj.lianjia.com/ershoufang/chaoyang/',
    # 'https://bj.lianjia.com/ershoufang/dongcheng/rs%E6%9C%9D%E9%98%B3/,'
    ]
    head = 'https://bj.lianjia.com'

    def parseDistricts(self, response):
      out = []
      ones = response.xpath('//*[@id="position"]/dl[2]/dd/div[1]/div[1]/a')
      for one in ones:
        urls = one.xpath('.//@href').extract()
        for url in urls:
          if url.startswith('http'):
            out.append(url)
          else:
            out.append(BasicSpider.head + url)

      return out


    def parse(self, response):
      # print(response)
      districts = self.parseDistricts(response)
      for one in districts:
        yield Request(one)

      ones = response.xpath('//*[@id="leftContent"]/ul/li')

      district = 'nan'
      d = response.xpath('//*[@id="position"]/dl[2]/dd/div[1]/div[1]/a[@class="selected"]/text()').extract()
      if len(d):
        district = d[0]

      nextPage = []
      nextPageText = ''.join(response.xpath('//*[@id="leftContent"]/div[8]/div[2]/div/a[last()]/text()').extract()).strip()
      if nextPageText == '下一页':
        nextPage.extend(response.xpath('//*[@id="leftContent"]/div[8]/div[2]/div/a[last()]/@href').extract())
      else:
        p = response.xpath('//*[@id="leftContent"]/div[8]/div[2]/div/a')
        # 框架支持url排重,这里就不排重了
        for one in p:
          nextPage.extend(one.xpath('.//@href').extract())

      for one in nextPage:
        nextURL = BasicSpider.head + one
        print('next url: %s'%(nextURL))
        yield Request(nextURL)

      for one in ones:
        oneOut = items.LianjiaHouseItem()
        oneOut['district'] = district
        oneOut['title'] = ''.join(one.xpath('.//div/div[1]/a/text()').extract()).strip()
        oneOut['_id'] = ''.join(one.xpath('.//div/div[1]/a/@data-housecode').extract()).strip()
        try:
          oneOut['building'] = ''.join(one.xpath('.//div/div[2]/div/a/text()').extract()).strip()
          oneOut['unitPrice'] = String2Number(''.join(one.xpath('.//div/div[4]/div[3]/div[2]/span/text()').extract()).strip())
          oneOut['totalPrice'] = String2Number(''.join(one.xpath('.//div/div[4]/div[3]/div[1]/span/text()').extract()).strip())

          oneOut['community'] = ''.join(one.xpath('.//div/div[2]/div/a/text()').extract())
          oneOut['houseType'] = ''.join(one.xpath('.//div/div[2]/div/text()[1]').extract())
          oneOut['square'] = String2Number(''.join(one.xpath('.//div/div[2]/div/text()[2]').extract()))

          oneOut['level'] = ''.join(one.xpath('.//div/div[3]/div/text()[1]').extract())
          if oneOut['level'][-1] == '万':
            oneOut['level'] = oneOut['level'][:-1]
          oneOut['structure'] = ''.join(one.xpath('.//div/div[3]/div/text()[2]').extract())
          oneOut['area'] = ''.join(one.xpath('.//div/div[3]/div/a/text()').extract())

          oneOut['attention'] = ''.join(one.xpath('.//div/div[4]/text()[1]').extract())
          oneOut['follow'] = ''.join(one.xpath('.//div/div[4]/text()[2]').extract())
        except Exception as e:
          print(e)
        yield oneOut
