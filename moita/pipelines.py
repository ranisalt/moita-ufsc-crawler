# -*- coding: utf-8 -*-

import json
from collections import defaultdict
from datetime import datetime
from unidecode import unidecode
from .items import Subject
from .spiders.cagr import SEMESTER


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

def classes(item: Subject):
    for klass in item['classes']:
        yield [klass['id'], item['hours'], klass['vacancy'], klass['occupied'],
               klass['special'], klass['remaining'], klass['lacking'],
               klass['raw_timetable'], klass['teachers']]
        del klass['raw_timetable']


class LegacyPipeline(object):
    data = defaultdict(list)
    time_format = '{}.{}-{} / {}'

    def process_item(self, item: Subject, spider):
        norm = unidecode(item['name']).upper()
        subject = [item['id'], norm, item['name'], list(classes(item))]
        self.data[item['campus']].append(subject)
        return item

    def close_spider(self, spider):
        self.data['DATA'] = datetime.now().strftime('%d/%m/%y - %H:%M')
        with open('{}.json'.format(SEMESTER), 'w') as fp:
            json.dump(self.data, fp, ensure_ascii=False, separators=(',', ':',))
