# -*- coding: utf-8 -*-
import scrapy
import ast
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
                return{
                png=splash:png(),
                url=splash:url(),
                }
            end
            """
    script1 = """
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
                assert(splash:wait(4))
                splash:set_viewport_full()
                return {
                url=splash:url(),
                png=splash:png(),
                }
            end
    
    """

    script2 = """
                function main(splash)
                    assert(splash:go(splash.args.url))
                    assert(splash:wait(3))
                    element2= assert(splash:select('p > a[href*="www.ingrammicrocloud.es/2014/05/30/what-does-amazons-bitcoin-move-mean-for-b2b-cloud-sales"]'))
                    assert(element2:mouse_click())
                    assert(splash:wait(4))
                    splash:set_viewport_full()
                    return {
                    png=splash:png(),
                    url=splash:url(),
                    }
                end
           """
    script3 = """
                function main(splash)
                                assert(splash:go(splash.args.url))
                                assert(splash:wait(4))
                                element= assert(splash:select('#menu-item-4674'))
                                assert(element:mouse_hover{x=0,y=0})
                                assert(splash:wait(4))
                                element2 = assert(splash:select('#menu-item-5131'))
                                assert(element2:mouse_click())
                                assert(splash:wait(4))
                                splash:set_viewport_full()
                                return {
                                png=splash:png(),
                                url=splash:url(),
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
        body = ast.literal_eval(response.body)
        imgstring = body['png']
        url = body['url']
        print "processing: " + url
        Image = "LandingPage Screenshot.png"
        fh= open(Image, "wb")
        fh.write(imgstring.decode('base64'))
        fh.close()
        print Image + " has been saved"
        yield SplashRequest(
            url=response.url,
            callback=self.parse2,
            endpoint='execute',
            args={'lua_source': self.script1},
        )

    def parse2(self,response):
        body = ast.literal_eval(response.body)
        png_bytes2 = body['png']
        url = body['url']
        print "processing: " + url
        Image = "Blog Screenshot.png"
        fh = open(Image, "wb")
        fh.write(png_bytes2.decode('base64'))
        fh.close()
        print Image + " has been saved"
        yield SplashRequest(
            url=response.url,
            callback=self.parse3,
            endpoint='execute',
            args={'lua_source': self.script2},
        )

    def parse3(self,response):
        body = ast.literal_eval(response.body)
        png_bytes3 = body['png']
        url = body['url']
        print "processing: " + url
        Image = "Post Screenshot.png"
        fh = open(Image, "wb")
        fh.write(png_bytes3.decode('base64'))
        fh.close()
        print Image + " has been saved"
        yield SplashRequest(
            url=response.url,
            callback=self.parse4,
            endpoint='execute',
            args={'lua_source': self.script3},
        )

    def parse4(self,response):
        body = ast.literal_eval(response.body)
        png_bytes3 = body['png']
        url = body['url']
        print "processing: " + url
        Image = "Quienes somos.png"
        fh = open(Image, "wb")
        fh.write(png_bytes3.decode('base64'))
        fh.close()
        print Image + " has been saved"
