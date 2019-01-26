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

    """
        Primer Script: 
        Renderizado de la pagina inicial y retorno de foto
    """

    script = """
            function pad(r, pad)
                return {r[1]-pad, r[2]-pad, r[3]+pad, r[4]+pad}
            end
            function main(splash)
                splash:set_viewport_size(1920, 1080)
                assert(splash:go(splash.args.url))
                assert(splash:wait(1))
                splash:set_viewport_full()
                return{
                png=splash:png(),
                url=splash:url(),
                }
            end
            """
    """
        Segundo Script:
        En la pagina inicial, interacciona con el menu, y va a la pagina del blog    
    """


    script1 = """
            function main(splash)
                	splash:set_viewport_size(1920, 1080)
	                assert(splash:go(splash.args.url))
                    assert(splash:wait(5))
                    menu=splash:select('#block-mainnavigation > div > ul > li:nth-of-type(4)')
                    assert(menu:mouse_click{})
                    assert(splash:wait(5))
                    element=splash:select('a[href*="blog"]')
                    assert(element:mouse_click{})
                    assert(splash:wait(5))
                    splash:set_viewport_full()
                    splash:set_viewport_full()
                return {
                url=splash:url(),
                png=splash:png(),
                }
            end
    """

    """
    Tercer Script:
    En el blog, va clickando en el siguiente boton, hasta que el elemento al que queremos redirigirnos aparezca    
    """


    script2 = """
                function main(splash)
                                assert(splash:go(splash.args.url))
                                assert(splash:wait(2))
                                element= splash:select('a[href*="/blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live/"]')
                                while (element == nil) do
                                        print(splash:url())
                                        nextbutton = splash:select('a[title*="Go to next page"]')
                                        assert(nextbutton:mouse_click())
                                        assert(splash:wait(2))
                                        element= splash:select('a[href*="/blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live/"]')
                                end
                                assert(splash:wait(2))
                                splash:set_viewport_full()
                                return{
                                png=splash:png(),
                                url=splash:url(),
                                }
                end
           """

    """
    Cuarto Script:
    Lo mismo que antes, solo que esta vez interactuamos con el elemento, y sacamos una foto de la pagina del blog    
    """


    script3 = """
                function main(splash)
                                assert(splash:go(splash.args.url))
                                assert(splash:wait(2))
                                element= splash:select('a[href*="/blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live/"]')
                                while (element == nil) do
                                        print(splash:url())
                                        nextbutton = splash:select('a[title*="Go to next page"]')
                                        assert(nextbutton:mouse_click())
                                        assert(splash:wait(2))
                                        element= splash:select('a[href*="/blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live/"]')
                                end
                                assert(element:mouse_click{})
                                assert(splash:wait(3))
                                splash:set_viewport_full()
                                return{
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
        Image = "Image-1.png"
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
        Image = "Image-2.png"
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
        Image = "Image-3.png"
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
        Image = "Image-4.png"
        fh = open(Image, "wb")
        fh.write(png_bytes3.decode('base64'))
        fh.close()
        print Image + " has been saved"
        yield SplashRequest(
            url=self.url,
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
