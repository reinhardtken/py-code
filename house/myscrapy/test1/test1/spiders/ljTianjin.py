# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-esf-tj'
    city = '天津'
    allowed_domains = [
      'tj.lianjia.com',
                       ]
    start_urls = [
      'https://tj.lianjia.com/ershoufang/heping/',
    ]
    head = 'https://tj.lianjia.com'

    collectionName = 'tianjin'

