# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Compose

class LeroymparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    category = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(
        input_processor=MapCompose(
            lambda x: x.replace(' ',''), lambda x: int(x)
        ),
        output_processor=TakeFirst()
    )
    pictures = scrapy.Field(input_processor=MapCompose())
    pass
