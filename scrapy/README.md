# TFG

Splash server
-------------

This code requires a splash server listening on port 8050.

The easiest way to obtain it is using the scrapinghub/splash docker image, available in standar docker hub.  It can be started and downloaded with the following docker command.

docker run -p 8050:8050 scrapinghub/splash

More details of splash use with scrapy in:

https://github.com/scrapy-plugins/scrapy-splash

https://splash.readthedocs.io/en/stable/index.html

Scrapy and Scrapy-splash module
-------------------------------

The following python modules must be installed with pip (already added to the requirements.txt file):

- scrapy  :  Spider-like HTTP scrapper.
- scrapy-splash : Plugin connector of scrapy with splash


TFG con Scrapy

Para quitar error de 'HtmlResponse' object has no attribute 'xpath' in scrapy:
https://stackoverflow.com/questions/33407140/i-am-getting-an-attributeerror-htmlresponse-object-has-no-attribute-xpath-i


