# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-esf-hf'
    city = '合肥'
    allowed_domains = [
      'hf.lianjia.com',
                       ]
    start_urls = [
      'https://hf.lianjia.com/ershoufang/baohe/',
    ]
    head = 'https://hf.lianjia.com'

    collectionName = 'hefei'

    xpath = spiders.ljShanghai.Spider.xpath
    xpath['districts'] = '/html/body/div[3]/div/div[1]/dl[2]/dd/div/div[1]/a'
    xpath['districtName'] = '/html/body/div[3]/div/div[1]/dl[2]/dd/div/div[1]/a[@class="selected"]/text()'