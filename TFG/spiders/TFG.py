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
                assert(splash:wait(1))
                splash:set_viewport_full()
                return splash:png{}
            end
            """
    script1 = """
            function main(splash)
                assert(splash:go(splash.args.url))
                assert(splash:wait(0.5))
                element=splash:select('a[href*="blog"]')
                assert(element:mouse_click{})
                assert(splash:wait(2))
                caja=splash:select('#searchform')
                caja:send_text('amazon')
                assert(caja:mouse_click())
                caja:submit()
                assert(splash:wait(2))
                splash:set_viewport_full()
                return {
                png=splash:png{},
                url=splash:url(),
                }
            end
    
    """

    script2 = """
                function main(splash)
                    assert(splash:go(splash.args.url))
                    assert(splash:wait(1.5))
                    element2= assert(splash:select('a[href*="www.ingrammicrocloud.es/2014/05/30/what-does-amazons-bitcoin-move-mean-for-b2b-cloud-sales"]'))
                    assert(element2:mouse_click())
                    assert(splash:wait(2))
                    splash:set_viewport_full()
                    return splash:png{}
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
        imgstring = response.body
        url = response.url
        print "processing: " + url
        Image= "LandingPage Screenshot.png"
        with open(Image, 'wb') as f:
            f.write(imgstring)
        print Image + " has been saved"
        yield SplashRequest(
            url=response.url,
            callback=self.parse2,
            endpoint='execute',
            args={'lua_source': self.script1},
        )

    def parse2(self,response):
        png_bytes2 = response.body
        url = response.url
        print "processing: " + url
        Image = "Blog Screenshot.png"
        with open(Image, 'wb') as f:
            f.write(png_bytes2)
        print Image + " has been saved"
        yield SplashRequest(
            url=response.url,
            callback=self.parse3,
            endpoint='execute',
            args={'lua_source': self.script2},
        )

    def parse3(self,response):
        png_bytes2 = response.body
        url = response.url
        print "processing: " + url
        Image = "Post Screenshot.png"
        with open(Image, 'wb') as f:
            f.write(png_bytes2)
        print Image + " has been saved"
