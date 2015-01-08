from setuptools import setup

__author__ = 'ranisalt'

def read(file):
    with open(file) as f:
        content = f.read()
    return content

setup(
    name='moita-scrapy',
    version='0.1.0',
    description='Simple scraper for UFSC list of subjects and classes with support to MongoDB',
    license='MIT',
    author=__author__,
    url='https://github.com/ranisalt/moita-scrapy',
    install_requires=read('requirements.txt'),
)