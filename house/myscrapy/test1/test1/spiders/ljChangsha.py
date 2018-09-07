# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-esf-cs'
    city = '长沙'
    allowed_domains = [
      'cs.lianjia.com',
                       ]
    start_urls = [
      'https://cs.lianjia.com/ershoufang/yuhua/',
    ]
    head = 'https://cs.lianjia.com'

    collectionName = 'changsha'