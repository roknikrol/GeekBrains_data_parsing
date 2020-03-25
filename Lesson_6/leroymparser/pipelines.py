# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os, os.path
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from Lesson_6.leroymparser import settings as sets
from scrapy.exceptions import DropItem

class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.avito_photo

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['pictures']:
            for img in item['pictures']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        for results in [x for ok, x in results if ok]:
            path = results['path']
            cat_name = item['category']

            storage = sets.IMAGES_STORE

            target_path = os.path.join(storage,cat_name,os.path.basename(path))
            path = os.path.join(storage,path)

            # If path doesn't exist, it will be created
            if not os.path.exists(os.path.join(storage,cat_name)) :
                os.makedirs(os.path.join(storage,cat_name ))

            if not os.rename(path,target_path) :
                raise DropItem("Could not move image to target folder")

        if self.IMAGES_RESULT_FIELD in item.fields :
            item[self.IMAGES_RESULT_FIELD] = [x for ok,x in results if ok]
        return item