# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LanvshenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    idd = scrapy.Field()
    title = scrapy.Field()
    shoot = scrapy.Field()
    quantity = scrapy.Field()
    name = scrapy.Field()
    nickname = scrapy.Field()
    birthday = scrapy.Field()
    height = scrapy.Field()
    _id = scrapy.Field()
