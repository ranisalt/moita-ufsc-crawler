# -*- coding: utf-8 -*-
import logging
import re
from scrapy.spiders.init import InitSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector

from moita.items import Campus
from moita.settings import AUTH_OPTIONS, SEMESTER, TIMES


class CagrSpider(InitSpider):
    name = "cagr"

    # data related to the service we want to scrap
    allowed_domains = ['sistemas.ufsc.br']
    login_url = 'http://sistemas.ufsc.br/login'
    start_urls = (
        'https://cagr.sistemas.ufsc.br/modules/aluno/cadastroTurmas/index.xhtml',
    )

    # space where data will be scraped before yield
    data = {}

    # there is a need to keep the first page form here
    index = None

    # regex to collect time data from the tables
    time_regex = re.compile('(?P<day>\\d).(?P<time>\\d{4}).(?P<qty>\\d+)\\W*(?P<room>\\S*\\b)')

    # self explaining
    current_campus = None
    current_page = None
    current_subject = None

    def init_request(self):
        logging.info("Authenticating session")
        return Request(url=self.login_url, callback=self.login)

    def login(self, response):
        return FormRequest.from_response(response, formdata=AUTH_OPTIONS, callback=self.auth_check)

    def auth_check(self, response):
        # login URL redirects us to a page where we can detect if auth was successful
        if "Sucesso ao se logar" in response.body:
            logging.info("Authentication successful")
            return Request(url=self.start_urls[0], callback=self.gather, dont_filter=True)
        else:
            logging.error("Authentication failed")

    def gather(self, response):
        # this method gathers data about all campi that will be scraped
        hxs = Selector(response)

        xcampi = hxs.xpath('//select[@id="formBusca:selectCampus"]/option[@value]')
        self.campus_name = [None] * len(xcampi)
        for xcampus in xcampi:
            _id = int(xcampus.xpath('@value').extract_first().strip())
            campus = xcampus.xpath('text()').extract_first().strip()[len('UFSC/'):]
            self.campus_name[_id] = campus

        self.index = response

        # scraping backwards seems faster AND the smaller campi are the last ones in the dropdown, so there is no need
        # to wait for the huge ones to scrap (or fail) to update the faster ones. it's just cosmetic.
        self.current_campus = len(xcampi) - 1
        self.current_page = 1

        return self.initialized()

    def make_requests_from_url(self, url=None):
        logging.info('Crawling %(campus)s on page %(page)d' % {
            'campus': self.campus_name[self.current_campus],
            'page': self.current_page,
        })

        # welp remember that I said I need to save the first page form? :)
        return FormRequest.from_response(self.index, formdata={
            'AJAXREQUEST': '_viewRoot',
            'formBusca:dataScroller1': str(self.current_page),
            'formBusca:selectCampus': str(self.current_campus),
            'formBusca:selectSemestre': SEMESTER,
        }, formname="formBusca", dont_filter=True)

    def parse(self, response):
        hxs = Selector(response, type='html')

        xtable = hxs.xpath('//tbody[@id="formBusca:dataTable:tb"]/tr')
        for xrow in xtable:
            xcells = [cell for cell in xrow.xpath('.//td')]

            # these steps are performed to insert a new subject if the current row represents a subject that was not yet
            # scraped, and add it before continuing on scraping classes

            subject_id = xcells[3].xpath('./text()').extract_first()
            if subject_id != self.current_subject:
                if self.data:
                    yield self.data

                self.current_subject = subject_id

                name = xcells[5].xpath('./text()').extract_first().strip()
                hours = int(xcells[6].xpath('./text()').extract_first().strip())

                self.data = {
                    '_id': subject_id,
                    'campus': self.campus_name[self.current_campus],
                    'semester': SEMESTER,
                    'name': name,
                    'hours': hours,
                    'classes': [],
                }

            class_id = xcells[4].xpath('./text()').extract_first().strip()
            vacancy = int(xcells[7].xpath('./text()').extract_first().strip())
            occupied = int(xcells[8].xpath('./text()').extract_first().strip())
            special = int(xcells[9].xpath('./text()').extract_first().strip())

            timetable = []
            for time in xcells[12].xpath('./text()').extract():
                stripped = self.time_regex.search(time).groupdict()

                # I opted to store an array of timespans that classes occupied instead of storing the starting time and
                # length of a class for simplicity at the front end. you may change to suit your needs or just use the
                # length of the "time" value
                timetable.append({
                    'day': int(stripped['day']),
                    'room': stripped['room'],
                    'time': TIMES[TIMES.index(stripped['time']):][:int(stripped['qty'])],
                })

            teachers = [teacher.strip() for teacher in xcells[13].xpath('.//a/text()').extract()]

            self.data['classes'].append({
                '_id': class_id,
                'vacancy': vacancy,
                'occupied': occupied,
                'special': special,
                'timetable': timetable,
                'teachers': teachers,
            })

        # detect if we are at the last page: if there is no non-active (other pages) buttons after active ones (current
        # page), then the current page must be the last one
        xbuttons = hxs.xpath('//table[@id="formBusca:dataScroller1_table"]/tbody/tr/td').css(
            '.rich-datascr-act + .rich-datascr-inact')
        if len(xbuttons) > 0:
            self.current_page += 1
        else:
            yield self.data
            # remember to increase instead of decrease if you start at the zeroth campus
            self.current_campus -= 1
            self.current_page = 1

        # and also remember to set this to < len(self.data) if you start at zero too.
        if self.current_campus >= 0:
            yield self.make_requests_from_url()
