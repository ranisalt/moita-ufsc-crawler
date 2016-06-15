# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import Subject


class SubjectPipeline(object):
    def process_item(self, item, spider):
        assert isinstance(item, dict)
        return Subject(**item)
