# -*- coding: utf-8 -*-

import spiders.turnover.ljBeijing2


class Spider(spiders.turnover.ljBeijing2.Spider):
  name = 'lianjia-cj-sh'
  city = '上海'
  allowed_domains = [
    'sh.lianjia.com',
  ]
  start_urls = [
    'https://sh.lianjia.com/chengjiao/pudong/',
  ]
  head = 'https://sh.lianjia.com'

  collectionName = 'shanghai'