# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    _id = scrapy.Field()
    district = scrapy.Field()
    unitPrice = scrapy.Field()
    totalPrice = scrapy.Field()
    pass
