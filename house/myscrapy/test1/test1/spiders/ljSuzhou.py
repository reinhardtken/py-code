# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-esf-su'
    city = '苏州'
    allowed_domains = [
      'su.lianjia.com',
                       ]
    start_urls = [
      'https://su.lianjia.com/ershoufang/gongyeyuan/',
    ]
    head = 'https://su.lianjia.com'

    collectionName = 'suzhou'

