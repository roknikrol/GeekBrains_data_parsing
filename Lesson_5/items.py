# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    # salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_net_gross = scrapy.Field()
    salary_currency = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    pass
