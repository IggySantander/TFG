# -*- coding: utf-8 -*-
import scrapy

import base64
from scrapy_splash import SplashRequest


class HomeSpider(scrapy.Spider):
    name = 'TFG'
    allowed_domains = ['us.dev.cloud.im']
    start_urls = 'https://us.dev.cloud.im'

    def start_requests(self):
        yield SplashRequest(
            url=HomeSpider.start_urls,
            callback=self.parse,
            endpoint='render.json',
            args={'wait': 2, 'html': 1, 'png': 1, 'render_all': 1}
        )

    def parse(self, response):
        title = response.css('title').extract_first()

        # full decoded JSON data is available as response.data:
        png_bytes = base64.b64decode(response.data['png'])

        print title
        print response.data

        with open('somefile.png', 'wb') as the_file:
            the_file.write(png_bytes)
