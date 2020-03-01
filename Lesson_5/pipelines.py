# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.exceptions import DropItem

class JobparserPipeline(object):
    def __init__(self):
        clinet = MongoClient('localhost', 27017)
        self.mongobase = clinet.vacancy_scrapy
##
    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        if collection.find({'link': item.get('link')}).count() > 0:
            DropItem("Already in DB" % item)
        else:
            collection.insert_one(item)
        return item
