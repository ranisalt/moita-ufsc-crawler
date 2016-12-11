# -*- coding: utf-8 -*-

import json
from collections import defaultdict, namedtuple
from datetime import datetime
from unicodedata import normalize
from .items import Subject
from .spiders.cagr import SEMESTER


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class LegacyPipeline(object):
    time_format = '{}.{}-{} / {}'

    def open_spider(self, spider):
        self.data = defaultdict(list)

    def process_item(self, item: Subject, spider):
        raw_classes = []
        for klass in item['classes']:
            raw_classes.append([
                klass['id'], item['hours'], klass['vacancy'], klass['occupied'],
                klass['special'], klass['remaining'], klass['lacking'],
                klass['raw_timetable'], klass['teachers']
            ])
            del klass['raw_timetable']

        try:
            norm = normalize('NFKD', item['name']).encode('ascii', 'ignore')
        except TypeError:
            norm = item['name']
        raw_subject = [
            item['id'], norm.upper(), item['name'], raw_classes
        ]

        self.data[item['campus']].append(raw_subject)
        return item

    def close_spider(self, spider):
        start_time = datetime.now()

        data = {
            'DATA': start_time.strftime('%d/%m/%y - %H:%M'),
        }

        data.update(self.data)

        semester = 1 if start_time.month < 7 else 2
        with open('{}.json'.format(SEMESTER), 'w') as fp:
            json.dump(data, fp, ensure_ascii=False, separators=(',', ':',))
