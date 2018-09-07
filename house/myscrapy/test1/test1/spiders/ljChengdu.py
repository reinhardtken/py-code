# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-esf-cd'
    city = '成都'
    allowed_domains = [
      'cd.lianjia.com',
                       ]
    start_urls = [
      'https://cd.lianjia.com/ershoufang/jinjiang/',
    ]
    head = 'https://cd.lianjia.com'

    collectionName = 'chengdu'