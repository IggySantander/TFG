# -*- coding: utf-8 -*-
import scrapy

import base64
from scrapy_splash import SplashRequest


class HomeSpider(scrapy.Spider):
    name = 'TFG'
    allowed_domains = ['ingrammicrocloud.es']
    start_urls = 'http://www.ingrammicrocloud.es/'
    script = """
            function pad(r, pad)
                return {r[1]-pad, r[2]-pad, r[3]+pad, r[4]+pad}
            end
            function main(splash)
                assert(splash:go(splash.args.url))
                assert(splash:wait(0.5))
                element=splash:select('a[href*="blog"]')
                assert(element:mouse_click{})
                assert(splash:wait(3))
                caja=splash:select('#searchform')
                caja:send_text('amazon')
                assert(caja:mouse_click())
                caja:submit()
                assert(splash:wait(3))
                splash:set_viewport_full()
                return {
                splash:png{},
                url = splash:url(),
                }
            end
            """
    def start_requests(self):
        yield SplashRequest(
            url=HomeSpider.start_urls,
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': self.script},
        )




    def parse(self, response):
        # full decoded JSON data is available as response.data:
        png_bytes = response.body
        with open('somefile.png', 'wb') as the_file:
            the_file.write(png_bytes)
        url = response.url
        print url

