# -*- coding: utf-8 -*-
import json
from scrapy.exporters import BaseItemExporter

from moita.settings import CAMPI, SEMESTER


class FilePipeline(BaseItemExporter):
    subjects = {campus: [] for campus in CAMPI}

    def process_item(self, item, spider):
        _item = dict(self._get_serialized_fields(item))
        self.subjects[_item['campus']].append(_item)

        return item

    def close_spider(self, spider):
        for campus in self.subjects:
            print(campus)
            with open(''.join([campus, str(SEMESTER), '.json']), 'w') as fp:
                json.dump(self.subjects[campus], fp)
