# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Subject(scrapy.Item):
    id = scrapy.Field()
    campus = scrapy.Field()
    semester = scrapy.Field()
    name = scrapy.Field()
    hours = scrapy.Field()
    classes = scrapy.Field()
