# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-nj'
    allowed_domains = [
      'nj.lianjia.com',
                       ]
    start_urls = [
      'https://nj.lianjia.com/ershoufang/gulou/',
    ]
    head = 'https://nj.lianjia.com'
    dbName = 'house'
    collectionName = 'nanjing'