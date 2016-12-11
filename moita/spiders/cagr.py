# -*- coding: utf-8 -*-
import collections
import os
import re

import scrapy
from scrapy.http import FormRequest, Request, Response

from ..items import Subject

SEMESTER = '20171'
TIMES = ['0730', '0820', '0910', '1010', '1100', '1330', '1420', '1510', '1620',
         '1710', '1830', '1920', '2020', '2110']


class CagrSpider(scrapy.Spider):
    name = 'cagr'
    allowed_domains = ['sistemas.ufsc.br']
    login_url = 'http://sistemas.ufsc.br/login'
    table_url = ('https://cagr.sistemas.ufsc.br/modules/aluno/'
                 'cadastroTurmas/index.xhtml')

    # current campus and subject being scraped
    campus, subject = tuple(), dict()
    campi_names, index = collections.OrderedDict(), None
    time_regex = re.compile(
        '(?P<day>\\d).(?P<time>\\d{4}).(?P<qty>\\d+)\\W*(?P<room>\\S*\\b)')

    def start_requests(self):
        def populate(res):
            if 'collecta.sistemas.ufsc.br' in res.url:
                return FormRequest.from_response(res, 'j_id20',
                                                 callback=populate)

            for campus in res.css('[id="formBusca:selectCampus"] option'):
                id_ = campus.css('::attr(value)').extract_first().strip()
                name = campus.css('::text').extract_first().strip()[5:]
                self.campi_names[id_] = name

            self.campus, self.index = self.campi_names.popitem(), res
            return self.make_requests_from_index(page=1)

        def post_login(res):
            # login URL redirects to a page where we can detect if successful
            if 'Sucesso ao se logar'.encode(res.encoding) in res.body:
                self.logger.debug('Authentication successful')
                return Request(self.table_url, populate, dont_filter=True)
            self.logger.error('Authentication failed')

        def pre_login(res):
            self.logger.debug('Authenticating session')
            return FormRequest.from_response(res, formdata={
                'username': self.settings.get('CAGR_USERNAME'),
                'password': self.settings.get('CAGR_PASSWORD'),
            }, callback=post_login)

        return Request(url=self.login_url, callback=pre_login),

    def make_requests_from_index(self, page):
        return FormRequest.from_response(self.index, 'formBusca', formdata={
            'AJAXREQUEST': '_viewRoot',
            'formBusca:dataScroller1': str(page),
            'formBusca:selectCampus': self.campus[0],
            'formBusca:selectSemestre': SEMESTER,
        }, callback=self.parse, dont_filter=True)

    def parse(self, res):
        def parse_timetable(timetable):
            t = self.time_regex.search(timetable)
            if t is None:
                return {}

            timeIndex = TIMES.index(t.group('time'))
            return {
                'day': int(t.group('day')),
                'room': t.group('room'),
                'time': TIMES[timeIndex:timeIndex + int(t.group('qty'))],
            }

        html = scrapy.Selector(text=res.body, type='html')

        for row in html.css('[id="formBusca:dataTable:tb"] tr'):
            cells = row.css('td')

            id_ = cells[3].css('::text').extract_first()
            # reached end of subject data
            if id_ != self.subject.get('id'):
                if self.subject:
                    yield Subject(**self.subject)
                self.subject = {
                    'id': id_,
                    'campus': self.campus[1],
                    'semester': SEMESTER,
                    'name': cells[5].css('::text').extract_first(),
                    'hours': cells[6].css('::text').extract_first(),
                    'classes': [],
                }

            remaining = cells[10].css('::text').extract_first()
            lacking = cells[11].css('::text').extract_first()

            self.subject['classes'].append({
                'id': cells[4].css('::text').extract_first(),
                'vacancy': int(cells[7].css('::text').extract_first()),
                'occupied': int(cells[8].css('::text').extract_first()),
                'special': int(cells[9].css('::text').extract_first()),
                'remaining': 0 if remaining == 'LOTADA' else int(remaining),
                'lacking': 0 if lacking is None else int(lacking),
                'raw_timetable': cells[12].css('::text').extract(),
                'timetable': [parse_timetable(time) for time in
                              cells[12].css('::text').extract()],
                'teachers': cells[13].css('::text').extract(),
            })

        page_buttons = html.css('.rich-datascr-act + .rich-datascr-inact')
        # an inactive button after an active means there's pages left
        if len(page_buttons) > 0:
            page = int(html.css('.rich-datascr-act::text').extract_first()) + 1
            yield self.make_requests_from_index(page=page)

        # reached end of campus data
        else:
            yield self.subject

            # move to next campus if there is any
            if self.campi_names:
                self.campus, self.subject = self.campi_names.popitem(), {}
                yield self.make_requests_from_index(page=1)
