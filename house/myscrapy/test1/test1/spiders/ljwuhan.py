# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-wh'
    city = '武汉'
    allowed_domains = [
      'wh.lianjia.com',
                       ]
    start_urls = [
      'https://wh.lianjia.com/ershoufang/jiangan/',
    ]
    head = 'https://wh.lianjia.com'
    dbName = 'house'
    collectionName = 'wuhan'