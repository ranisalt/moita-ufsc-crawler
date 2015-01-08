# -*- coding: utf-8 -*-
import json
from scrapy.contrib.exporter import BaseItemExporter


class CagrPipeline(object):
    @staticmethod
    def process_item(item, spider):
        # this step is needed because subjects are a list, so indexes must be removed
        # indexes are useful while scraping to improve subject manipulation
        item['subjects'] = item['subjects'].values()

        return item


class FilePipeline(BaseItemExporter):
    def process_item(self, item, spider):
        _item = dict(self._get_serialized_fields(item))

        with open(''.join([_item['campus'], _item['semester'], '.json']), 'w') as fp:
            fp.write(json.dumps(_item))

        return item