# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DebugItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class MTItem(scrapy.Item):
    city = scrapy.Field()
    title = scrapy.Field()
    avgPrice = scrapy.Field()
    address = scrapy.Field()
    avgScore = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()