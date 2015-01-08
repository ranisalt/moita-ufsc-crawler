This repository contains a new scraper to extract data from CAGR's database to be used with CAPIM and derivatives. It 
comes with a MongoDB pipeline as an example of what can be done with a flexible scraping framework such as Scrapy.

**moita-scrapy** first logs in with credentials provided at [moita/settings.py](moita/settings.py), then proceeds to the
data table and gathers necessary data to start scraping. The crawler is very simple, with less than 150 lines and most
of them are needed just because CAGR is overly complex and bad designed.

To use your own pipeline (for example, if you want to dump extracted data to a file instead of using a database), please
refer to Scrapy documentation. Links to relevant documentation pages are included at the top of each file.

To change the format of resulting scraped data, please read the *parse* function inside *CagrSpider* at
[moita/spiders/cagr.py](moita/spiders/cagr.py). Currently, data is gathered as follows:

Campus:
- campus id (int), e.g.: 1 for FLO
- campus name (str), e.g.: FLO for Florianópolis
- campus subjects (list):
  - subject id (str), e.g. INE5401
  - subject name (str), e.g. Introdução à Computação
  - subject hours (int), e.g. 36
  - subject classes (list):
    - class id (str), e.g. 01208A
    - class vacancy (int), e.g. 50
    - class occupation (int), e.g. 35
    - class special spots (int), e.g. 5
    - class timetable (list):
      - time day (int), e.g. 2 for Monday
      - time room (str), e.g. AUX-ALOCAR
      - time time (sorry, list), e.g. ['1010', '1100'] if class starts at 10:10 and is 2 classes long
    - class teachers (list), e.g. ['Rafael Luiz Cancian', 'José Luis Güntzel']

Although it seems fairly complex, it is very easy to traverse and perform search operations, assuming you split into
several classes. The resultant JSON is about 3MB big and can be compressed down to about 200KB with gzip. The file can
be further reduced if you keep the original time format (e.g. `2.0820-2 / AUX-ALOCAR`) or removing default data (e.g.
when vacancy is 0) but it reduces the expressivity of the data while not reducing too much with gzip compression.

This crawler was inspired by the original one by [Ramiro Polla](@ramiropolla) which can be found at
[ramiropolla/matrufsc_dbs](https://github.com/ramiropolla/matrufsc_dbs), while trying to make data more useful and keep
code clean and readable, as long as web scraping and XPath could lead me.

**Observation:** this piece of software was made while my internet provider had blocked GitHub for some shady unknown
reason. That's why after some time I decided to give up on git versioning and just release when it was done. I should
return to normal versioning now that I cancelled the service.

This work is double licensed under the [MIT License](https://tldrlegal.com/license/mit-license) and
[Beerware License](https://tldrlegal.com/license/beerware-license).