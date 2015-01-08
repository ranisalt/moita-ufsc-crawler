# -*- coding: utf-8 -*-


class CagrPipeline(object):
    @staticmethod
    def process_item(item, spider):
        # this step is needed because subjects are a list, so indexes must be removed
        # indexes are useful while scraping to improve subject manipulation
        item['subjects'] = item['subjects'].values()

        return item