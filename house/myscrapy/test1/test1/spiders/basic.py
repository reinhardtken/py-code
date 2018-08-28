# -*- coding: utf-8 -*-
import scrapy

import items

class BasicSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['https://bj.lianjia.com/ershoufang/chaoyang/rs%E6%9C%9D%E9%98%B3/']

    def parse(self, response):
      print(response)
      ones = response.xpath('//*[@id="leftContent"]/ul/li')
      titles = response.xpath('//*[@id="leftContent"]/ul/li/div/div[1]/a').extract()
      houseCodes = response.xpath('//*[@id="leftContent"]/ul/li/div/div[1]/a/@data-housecode').extract()
      houses = response.xpath('//*[@id="leftContent"]/ul/li/div/div[2]/div/a').extract()
      totalPrices = response.xpath('//*[@id="leftContent"]/ul/li/div/div[4]/div[3]/div[1]/span').extract()
      prices = response.xpath('//*[@id="leftContent"]/ul/li/div/div[4]/div[3]/div[2]/span').extract()

      for one in ones:
        oneOut = items.LianjiaHouseItem()
        oneOut['title'] = ''.join(one.xpath('.//div/div[1]/a/text()').extract()).strip()
        oneOut['_id'] = ''.join(one.xpath('.//div/div[1]/a/@data-housecode').extract()).strip()
        oneOut['district'] = ''.join(one.xpath('.//div/div[2]/div/a/text()').extract()).strip()
        oneOut['unitPrice'] = ''.join(one.xpath('.//div/div[4]/div[3]/div[2]/span/text()').extract()).strip()
        oneOut['totalPrice'] = ''.join(one.xpath('.//div/div[4]/div[3]/div[1]/span/text()').extract()).strip()
        yield oneOut
