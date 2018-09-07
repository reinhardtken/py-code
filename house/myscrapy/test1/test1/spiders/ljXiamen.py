# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-esf-xm'
    city = '厦门'
    allowed_domains = [
      'xm.lianjia.com',
                       ]
    start_urls = [
      'https://xm.lianjia.com/ershoufang/siming/',
    ]
    head = 'https://xm.lianjia.com'

    collectionName = 'xiamen'