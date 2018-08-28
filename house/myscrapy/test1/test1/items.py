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
    # building = scrapy.Field()
    layout = scrapy.Field()
    unitPrice = scrapy.Field()
    totalPrice = scrapy.Field()

    # houseInfo = scrapy.Field()
    community = scrapy.Field()
    houseType = scrapy.Field()
    square = scrapy.Field()

    # positionInfo = scrapy.Field()
    level = scrapy.Field()
    structure = scrapy.Field()
    area = scrapy.Field()

    # followInfo = scrapy.Field()
    attention = scrapy.Field()
    follow = scrapy.Field()
    release = scrapy.Field()
    pass
