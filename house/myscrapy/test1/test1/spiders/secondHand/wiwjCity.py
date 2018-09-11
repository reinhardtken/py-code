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
  xpath = spiders.secondHand.wiwjBeijing.Spider.xpath
  xpath['nextPageText'] = '/html/body/div[4]/div[1]/div[2]/div[2]/a[1]/text()'
  xpath['nextPage'] = '/html/body/div[4]/div[1]/div[2]/div[2]/a[1]/@href'


class SpiderNJ(spiders.secondHand.wiwjBeijing.Spider):
  name = 'wiwj-esf-nj'
  city = '南京'
  allowed_domains = [
    'nj.5i5j.com',
  ]
  start_urls = [
    'https://nj.5i5j.com/ershoufang/jiangningqu/',
  ]
  head = 'https://nj.5i5j.com'

  collectionName = 'nanjing'





class SpiderSU(spiders.secondHand.wiwjBeijing.Spider):
  name = 'wiwj-esf-su'
  city = '苏州'
  allowed_domains = [
    'sz.5i5j.com',
  ]
  start_urls = [
    'https://sz.5i5j.com/ershoufang/yuanqu/',
  ]
  head = 'https://sz.5i5j.com'

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



class SpiderZZ(spiders.secondHand.wiwjBeijing.Spider):
  name = 'wiwj-esf-zz'
  city = '郑州'
  allowed_domains = [
    'zz.5i5j.com',
  ]
  start_urls = [
    'https://zz.5i5j.com/ershoufang/zhongyuanqu/',
  ]
  head = 'https://zz.5i5j.com'
  collectionName = 'zhengzhou'


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