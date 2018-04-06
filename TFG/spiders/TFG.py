# -*- coding: utf-8 -*-
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.linkextractors import LinkExtractor

from scrapy_splash import SplashRequest


class TFG(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    # http_user = 'splash-user'
    # http_pass = 'splash-password'

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            yield SplashRequest(
                link.url,
                self.parse_link,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )

    def parse_link(self, response):
        print("PARSED", response.real_url, response.url)
        print(response.css("title").extract())
        print(response.data["har"]["log"]["pages"])
        print(response.headers.get('Content-Type'))





#---------------------------

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(TFG)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished