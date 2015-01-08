# -*- coding: utf-8 -*-

# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Campus(scrapy.Item):
    _id = scrapy.Field()
    campus = scrapy.Field()
    semester = scrapy.Field()
    subjects = scrapy.Field()