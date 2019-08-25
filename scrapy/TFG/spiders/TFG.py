# -*- coding: utf-8 -*-
import scrapy
import ast
import base64
from scrapy_splash import SplashRequest
import re
from scrapy.linkextractors import LinkExtractor


class HomeSpider(scrapy.Spider):
    name = 'TFG'
    allowed_domains = ['ingrammicrocloud.com']
    start_urls = 'http://www.ingrammicrocloud.com/'
    blog_url = "https://www.ingrammicrocloud.com/blog/"

  # Initial script from first request

    script = """
             function pad(r, pad)
                    return {r[1]-pad, r[2]-pad, r[3]+pad, r[4]+pad}
                end   
            function main(splash)
                splash:set_viewport_size(1920, 1080)
                assert(splash:go(splash.args.url))
                assert(splash:wait(1))
                splash:set_viewport_full()
                -- Task 01: Accepting cookies and saving main page
                
                element=splash:select('.agree-button.btn.btn-secondary.btn-sm.custom_agree')
                assert(element:mouse_click{})
                assert(splash:wait(1))
                
                --Task 02: Getting all elements of menu
                local menu = {}
                local menu_text = {}
              	local submenu = {}
              	local submenu_text = {}
                    menu2 = splash:select_all('#header-')
                    submenu2 = splash:select_all('.link-box.link-box-small')
                    --for key,value in pairs(fields) do
                    --                    if (value:text() ~= "") then
                    --                       print(value.node:text())
                    --                        print(value.node:getAttribute('href'))
                    --                    end
                    --end
                    for i, elem in ipairs(menu2) do
                        table.insert(menu,elem:getAttribute('href')) 
                        table.insert(menu_text,elem:text())
                    end
  					for i, elem in ipairs(submenu2) do
                        table.insert(submenu,elem.node:getAttribute('href'))
                        table.insert(submenu_text,elem:text())
                    end
                
                
                
                -- Task 03: We enter the blog
                
                element= splash:select('#block-mainnavigation > div > ul > li:nth-of-type(4)')
                assert(element:mouse_click{})
                assert(splash:wait(1))
                return{
                menu=menu,
                menu_text=menu_text,
    			submenu=submenu,
    			submenu_text=submenu_text,
                png=splash:png(),
                url=splash:url(),
                }
            end
            """


    script1 = """
           function main(splash)
                splash:set_viewport_size(1920, 1080)
                assert(splash:go(splash.args.url))
                splash:set_viewport_full()
                assert(splash:wait(1))
                element= splash:select('#block-mainnavigation > div > ul > li:nth-of-type(4)')
                assert(element:mouse_click{})
                assert(splash:wait(1))
                element= splash:select('#header-Blog')
                assert(element:mouse_click{})
                assert(splash:wait(1))
                -- Task 04: Enter in a specific article
                
                element= splash:select('a[href*="/blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live/"]')
                                while (element == nil) do
                                        print(splash:url())
                                        nextbutton = splash:select('a[rel="next"]')
                                        assert(nextbutton:mouse_click())
                                        assert(splash:wait(1.5))
                                        element= splash:select('a[href*="/blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live/"]')
                                end
                assert(splash:wait(1))
                splash:set_viewport_full()
                return{
                png=splash:png(),
                url=splash:url(),
                }
            end
    """


    script2 = """
                treat = require('treat')
                function main(splash)
                                splash:set_viewport_size(1920, 1080)
                                assert(splash:go(splash.args.url))
                                assert(splash:wait(1))
                                -- Task 05:  Navigate back to the blog
                                element=splash:select('.logo')
                                assert(element:mouse_click{})
                                assert(splash:wait(1))
                                
                                -- Task 06 : Finding blog entries with date march 2019
                                
                                element= splash:select('#block-mainnavigation > div > ul > li:nth-of-type(4)')
                                assert(element:mouse_click{})
                                assert(splash:wait(1))
                                element= splash:select('#header-Blog')
                                assert(element:mouse_click{})
                                assert(splash:wait(1))
                                nextbutton = splash:select('a[rel="next"]')
                                while (nextbutton ~= nil) do
                                        print(splash:url())
                                        nextbutton = splash:select('a[rel="next"]')
                                        assert(nextbutton:mouse_click())
                                        assert(splash:wait(2))
                                        nextbutton = splash:select('a[rel="next"]')
                                end
                                local blogs = {}
                                local blogsmarch= splash:select_all('.blog-box')
                                
                                for i, elem in ipairs(blogsmarch) do
                                    table.insert(blogs,elem.node:getAttribute('href'))
                                end
                                
                                times= splash:select_all('a >  div:nth-child(2) > div:nth-child(3) > span:nth-child(1) > time:nth-child(1)')
                                
                                timestamp = {}
                                for i, elem in ipairs(times) do
                                    table.insert(timestamp,elem.node:text())
                                end
                                
                                -- Task 08: Find all countries and selecting Spain
                                element= splash:select('.selected-country')
                                assert(element:mouse_click{})
                                assert(splash:wait(1.5))
                                local hrefs = {}
                                local text = {}
                                elements=splash:select_all('a[href*="www.ingrammicrocloud"]')
                                
                                for i, elem in ipairs(elements) do
                                    if (elem:text() ~= "") then
                                        text[i]= elem.node:text()
                                        hrefs[i] = elem.node:getAttribute('href')
                                    end
                                end

                                splash:set_viewport_full()
                                return{
                                hrefs=hrefs,
                                text=text,
                                timestamp= timestamp,
                                blogs=blogs,
                                png=splash:png(),
                                url=splash:url(),
                                }
                end
           """


    script3 = """
               function main(splash)
  								splash:set_viewport_size(1920, 1080)
                                assert(splash:go(splash.args.url))
                                assert(splash:wait(1))
                                element= splash:select('a[href*=".com/es/es"]')
                                assert(element:mouse_click{})
                                assert(splash:wait(1))
                                -- Task 09: We select all articles in category partner stories
                                
                                element= splash:select('a[href*="/es/es/partner-stories/"]')
                                assert(element:mouse_click{})
                                assert(splash:wait(1))
                                local submenu= {}
                                local submenu_text = {}
                                local menu = {}
                                local menu_text = {}
                                for var=2,5 do
                                    element= splash:select('body > div.dialog-off-canvas-main-canvas > div.wrapper.background-light > div > div:nth-child(2) > div > ul > li:nth-child('..var ..')')
                                    if (element ~= nil) then
                                        table.insert(menu_text,element.node:text())
                                        table.insert(menu,element:getAttribute('href'))
                                    end
                                end
                                    campos = splash:select_all('.partner-box')
                                    for key,value in pairs(campos) do
                                        if (value:text() ~= "") then
                                        --print(value:text())
                                        --print(value:getAttribute('href'))
                                        table.insert(submenu_text,value.node:text())
                                        table.insert(submenu,value:getAttribute('href'))
                                        end
                                    end
                                    
                                
                                splash:set_viewport_full()
                                return{
                                menu=menu,
                                menu_text=menu_text,
                                submenu=submenu,
                                submenu_text=submenu_text,
                                png=splash:png(),
                                url=splash:url(),
                                }
                end
    """

 
    script4 = """
               function main(splash)
                        splash:set_viewport_size(1920, 1080)
                        assert(splash:go(splash.args.url))
                        assert(splash:wait(1))
                        splash:set_viewport_full()
                        -- Task 07: Fill in contact form
                        
                        element= splash:select('#block-mainnavigation > div > ul > li:nth-of-type(4)')
                        assert(element:mouse_click{})
                        assert(splash:wait(1))
                        element= splash:select('#header-Contact')
                        assert(element:mouse_click{})
                        assert(splash:wait(1))
                        element= splash:select('[name*="email"]')
                        element:send_text("test.1@hotmail.com")
                        assert(splash:wait(1))
                        element= splash:select('[type*="submit"]')
                        assert(element:mouse_click{})
                        assert(splash:wait(1))
                        return{
                                png=splash:png(),
                                url=splash:url(),
                        }   
                end
    """

    # Initial request

# In these requests/ responses, we will parse all the elements retrieved by scrapy/splash.

# Task 01: Accepting cookies and saving mainpage
# Task 02: Getting all elements of menu
# Task 03: We enter the blog
# Task 04: Enter in a specific article
# Task 05:  Navigate back to the blog
# Task 06: Finding blog entries with date march 2019
# Task 07: Fill in contact form
# Task 08: Find all countries and selecting Spain
# Task 09: We select all articles in category partner stories

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
        menu_text= body['menu_text']
        menu=body['menu']
        submenu_text=body['submenu_text']
        submenu=body['submenu']

        print "Menu Principal:"
        for elem in menu:
            print menu_text[elem]
            print menu[elem]

        print "Menus secundarios:"
        for elem in submenu:
            print submenu_text[elem]
            print submenu[elem]

        url = body['url']
        print "processing: " + url
        Image = "Image-1.png"
        fh = open(Image, "wb")
        fh.write(imgstring.decode('base64'))
        fh.close()
        print Image + " has been saved"
        yield SplashRequest(
            url=response.url,
            callback=self.parse2,
            endpoint='execute',
            args={'lua_source': self.script1},
        )


    def parse2(self, response):
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
            args={'lua_source': self.script2}
        )


    def parse3(self, response):
        body = ast.literal_eval(response.body)
        png_bytes3 = body['png']
        url = body['url']
        hrefs = body['hrefs']
        text = body['text']
        timestamp= body['timestamp']
        blogs=body['blogs']
        print "March 2019 blogs:"
        for entrie in timestamp:
            if "March" in timestamp[entrie]:
                if "2019" in timestamp[entrie]:
                    print blogs[entrie]
                    print timestamp[entrie]

        print "Countries available:"

        for elem in text:
            print  text[elem]
            print  hrefs[elem]



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



    def parse4(self, response):
        body = ast.literal_eval(response.body)
        png_bytes3 = body['png']
        url = body['url']
        menu_text = body['menu_text']
        menu = body['menu']
        submenu_text = body['submenu_text']
        submenu = body['submenu']

        print "Menu Principal:"
        for elem in menu:
            print menu_text[elem]
            print menu[elem]

        print "Menu¡s secundarios:"
        for elem in submenu:
            print submenu_text[elem]
            print submenu[elem]
        print "processing: " + url
        Image = "Image-4.png"
        fh = open(Image, "wb")
        fh.write(png_bytes3.decode('base64'))
        fh.close()
        print Image + " has been saved"
        yield SplashRequest(
            url=HomeSpider.start_urls,
            callback=self.parse5,
            endpoint='execute',
            args={'lua_source': self.script4},
        )

    def parse5(self, response):
        body = ast.literal_eval(response.body)
        png_bytes3 = body['png']
        url = body['url']
        print "processing: " + url
        Image = "Image-5.png"
        fh = open(Image, "wb")
        fh.write(png_bytes3.decode('base64'))
        fh.close()
        print Image + " has been saved"
