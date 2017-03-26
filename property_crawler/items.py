# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import  Item, Field

class PropertyCrawlerItem(Item):
    imageUrl = Field()
    propertyUrl = Field()
    propertyName  =Field()


class ImageItems(Item):
    image_urls = Field()
    images = Field()
    image_name = Field()
    directory = Field()

class AnnotationItems (Item):
    files = Field()
    file_urls  = Field()
    file_name = Field()
    directory = Field()


class PropertyImageItems(Item):
    image_urls = Field()
    images = Field()

