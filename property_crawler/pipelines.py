# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import time

import os, os.path
import json


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}".format(data))
        if valid:
            self.collection.insert(dict(item))
            return item


class DynamicPathImgPipeline(object):
    def process_item(self, item, spider):
        item_images = item['images']
        for image in item_images:
            print item['category']
            source_path = os.path.join(os.path.abspath("./images"), image['path'])
            image['path'] = image['path'].replace('full', item['category'][0])

            target_folder = os.path.join(os.path.abspath("./images") , item['category'][0])
            if not os.path.isdir(target_folder):
                os.makedirs(target_folder)

            target_path = os.path.join(os.path.abspath("./images"), image['path'])
            print source_path
            print target_path
            print "-"*20

            if not os.rename(source_path, target_path):
                raise Exception("Could not move image to target folder")

        return item

