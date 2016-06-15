from setuptools import find_packages, setup


setup(
    name='moita-scrapy',
    version='0.2.0',
    author='Ranieri Althoff',
    author_email='ranisalt@gmail.com',
    description='Scraper for UFSC table of subjects, classes and timetables',
    license='MIT',
    url='https://github.com/ranisalt/moita-scrapy',
    packages=find_packages(),
    entry_points = {'scrapy': ['settings = moita.settings']},
)
