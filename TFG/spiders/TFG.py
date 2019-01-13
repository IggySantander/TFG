# -*- coding: utf-8 -*-
import scrapy
import ast
import base64
from scrapy_splash import SplashRequest


class HomeSpider(scrapy.Spider):
    name = 'TFG'
    allowed_domains = ['ingrammicrocloud.com']
    start_urls = 'http://www.ingrammicrocloud.com/'
    blog_url = "https://www.ingrammicrocloud.com/blog/"
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
                                assert(splash:wait(2))
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

    script4 = """   
                    function main(splash)
                                assert(splash:go(splash.args.url))
                                assert(splash:wait(5))
                                element= splash:select('p > a[href*="http://www.ingrammicrocloud.es/2014/10/31/are-you-tired-of-one-size-fits-all-cloud-services/"]')
                                while (element == nil) do
                                        print(splash:url())
                                        nextbutton = splash:select('a[class*="next page-numbers"]')
                                        assert(nextbutton:mouse_click())
                                        assert(splash:wait(10))
                                        element= splash:select('p > a[href*="http://www.ingrammicrocloud.es/2014/10/31/are-you-tired-of-one-size-fits-all-cloud-services/"]')
                                end
                                assert(splash:wait(5))
                                splash:set_viewport_full()
                                return{
                                png=splash:png(),
                                url=splash:url(),
                                }
                    end
    
    
    
    
    
    """
    #Initial request
    def start_requests(self):
        yield SplashRequest(
            url=HomeSpider.start_urls,
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': self.script},
        )

        #First parse that saves the Landing Page image and then calls the next script
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
        #Escenario of imput text in a search box and then saving the results
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
        #Screenshot of the blog
        #Should be added a method to scrape the number of words

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

        #Scenario of combobox, same as cmp

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
        yield SplashRequest(
            url=self.blog_url,
            callback=self.parse5,
            endpoint='execute',
            args={'lua_source': self.script4,'timeout': 3600},
        )


        #Scenario of crawling pages until element matches
    def parse5(self,response):
        body = ast.literal_eval(response.body)
        png_bytes4 = body['png']
        url = body['url']
        print "processing: " + url
        Image = "Blog Crawling.png"
        fh = open(Image, "wb")
        fh.write(png_bytes4.decode('base64'))
        fh.close()
        print Image + " has been saved"
