# -*- coding: utf-8 -*-
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.linkextractors import LinkExtractor
import base64
from scrapy_splash import SplashRequest


class TFG(scrapy.Spider):
    name = 'extract'

    def start_requests(self):
        url = 'https://stackoverflow.com/'
        splash_args = {
            'html': 1,
            'png': 1
        }
        yield SplashRequest(url, self.parse_result, endpoint='render.json', args=splash_args)

    def parse_result(self, response):
        hxs = scrapy.Selector(response)
        for sel in hxs.xpath("//div[@id='job_listings']/a"):
            imgdata = base64.b64decode(response.data['png'])
            filename = 'some_image.png'
            with open(filename, 'wb') as f:
                f.write(imgdata)





#---------------------------

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(TFG)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished