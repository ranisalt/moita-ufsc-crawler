# -*- coding: utf-8 -*-

# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html

BOT_NAME = 'cagr'

SPIDER_MODULES = ['moita.spiders']
NEWSPIDER_MODULE = 'moita.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ufsc (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    # file pipeline used to write scraped JSON data to a file
    # if you do not change, filename is by default <campus><semester>.json, e.g. FLO20151.json
    # this SHOULD be higher than CagrPipeline
    'moita.pipelines.FilePipeline': 999,

    # mongodb pipeline used to write scraped data to collection
    # it can be replaced with a pipeline to save in a file or so
    # this SHOULD be higher than CagrPipeline
    #'scrapy_mongodb.MongoDBPipeline': 999,
}

LOG_LEVEL = 'INFO'

# MUST match CAGR times
TIMES = ['0730', '0820', '0910', '1010', '1100', '1330', '1420', '1510', '1620', '1710', '1830', '1920', '2020', '2110']

# MUST match CAGR dropdown
CAMPI = {
    'ARA': 'Araranguá',
    'BLN': 'Blumenau',
    'CBS': 'Curitibanos',
    'EaD': 'Ensino à Distância',
    'FLO': 'Florianópolis',
    'JOI': 'Joinville',
}

# MUST match CAGR valid semester
SEMESTER = '20161'
