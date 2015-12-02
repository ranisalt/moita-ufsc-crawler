# -*- coding: utf-8 -*-
import json
from scrapy.contrib.exporter import BaseItemExporter


class FilePipeline(BaseItemExporter):
    def process_item(self, item, spider):
        _item = dict(self._get_serialized_fields(item))

        with open(''.join([_item['campus'], _item['semester'], '.json']), 'w') as fp:
            fp.write(json.dumps(_item))

        return item
