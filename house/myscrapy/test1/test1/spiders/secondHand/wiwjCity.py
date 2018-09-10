# -*- coding: utf-8 -*-

import spiders.secondHand.wiwjBeijing


class SpiderCS(spiders.secondHand.wiwjBeijing.Spider):
  name = 'wiwj-esf-cs'
  city = '长沙'
  allowed_domains = [
    'cs.5i5j.com',
  ]
  start_urls = [
    'https://cs.5i5j.com/ershoufang/furongqu/',
  ]
  head = 'https://cs.5i5j.com'

  collectionName = 'changsha'


class SpiderSH(spiders.secondHand.wiwjBeijing.Spider):
  name = 'wiwj-esf-sh'
  city = '上海'
  allowed_domains = [
    'sh.5i5j.com',
  ]
  start_urls = [
    'https://sh.5i5j.com/ershoufang/pudongxinqu/',
  ]
  head = 'https://sh.5i5j.com'
  collectionName = 'shanghai'



class SpiderCD(spiders.secondHand.wiwjBeijing.Spider):
  name = 'wiwj-esf-cd'
  city = '成都'
  allowed_domains = [
    'cd.5i5j.com',
  ]
  start_urls = [
    'https://cd.5i5j.com/ershoufang/shuangliuqu/',
  ]
  head = 'https://cd.5i5j.com'

  collectionName = 'chengdu'


class SpiderTJ(spiders.secondHand.wiwjBeijing.Spider):
  name = 'wiwj-esf-tj'
  city = '天津'
  allowed_domains = [
    'tj.5i5j.com',
  ]
  start_urls = [
    'https://tj.5i5j.com/ershoufang/nankaiqu/',
  ]
  head = 'https://tj.5i5j.com'

  collectionName = 'tianjin'


class SpiderGZ(spiders.secondHand.wiwjBeijing.Spider):
  name = 'lianjia-cj-gz'
  city = '广州'
  allowed_domains = [
    'gz.lianjia.com',
  ]
  start_urls = [
    'https://gz.lianjia.com/chengjiao/tianhe/',
  ]
  head = 'https://gz.lianjia.com'

  collectionName = 'guangzhou'

class SpiderHZ(spiders.secondHand.wiwjBeijing.Spider):
  name = 'wiwj-esf-hz'
  city = '杭州'
  allowed_domains = [
    'hz.5i5j.com',
  ]
  start_urls = [
    'https://hz.5i5j.com/ershoufang/gongshuqu/',
  ]
  head = 'https://hz.5i5j.com'
  collectionName = 'hangzhou'


class SpiderNJ(spiders.secondHand.wiwjBeijing.Spider):
  name = 'lianjia-cj-nj'
  city = '南京'
  allowed_domains = [
    'nj.lianjia.com',
  ]
  start_urls = [
    'https://nj.lianjia.com/chengjiao/gulou/',
  ]
  head = 'https://nj.lianjia.com'

  collectionName = 'nanjing'





class SpiderSU(spiders.secondHand.wiwjBeijing.Spider):
  name = 'lianjia-cj-su'
  city = '苏州'
  allowed_domains = [
    'su.lianjia.com',
  ]
  start_urls = [
    'https://su.lianjia.com/chengjiao/gongyeyuan/',
  ]
  head = 'https://su.lianjia.com'

  collectionName = 'suzhou'


class SpiderWH(spiders.secondHand.wiwjBeijing.Spider):
  name = 'lianjia-cj-wh'
  city = '武汉'
  allowed_domains = [
    'wh.lianjia.com',
  ]
  start_urls = [
    'https://wh.lianjia.com/chengjiao/jiangan/',
  ]
  head = 'https://wh.lianjia.com'

  collectionName = 'wuhan'


class SpiderXM(spiders.secondHand.wiwjBeijing.Spider):
  name = 'lianjia-cj-xm'
  city = '厦门'
  allowed_domains = [
    'xm.lianjia.com',
  ]
  start_urls = [
    'https://xm.lianjia.com/chengjiao/siming/',
  ]
  head = 'https://xm.lianjia.com'

  collectionName = 'xiamen'


class SpiderXA(spiders.secondHand.wiwjBeijing.Spider):
  name = 'lianjia-cj-xa'
  city = '西安'
  allowed_domains = [
    'xa.lianjia.com',
  ]
  start_urls = [
    'https://xa.lianjia.com/chengjiao/beilin/',
  ]
  head = 'https://xa.lianjia.com'

  collectionName = 'xian'


# class SpiderZZ(spiders.secondHand.wiwjBeijing.Spider):
#   name = 'lianjia-cj-zz'
#   city = '郑州'
#   allowed_domains = [
#     'zz.lianjia.com',
#   ]
#   start_urls = [
#     'https://zz.lianjia.com/chengjiao/jinshui/',
#   ]
#   head = 'https://zz.lianjia.com'
#
#   collectionName = 'zhengzhou'