# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
import locale
import urlparse
import logging
from random import randint
from scrapy.crawler import CrawlerProcess


logger = logging.getLogger("Wimdu-Property-Crawler")
fh = logging.FileHandler("crawler.log")

fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)


from property_crawler.items import PropertyCrawlerItem

# x = response.xpath("//h3[@class='hit-headline']/a[@class='hit-url js-hitLink']/@href")[10].extract()


class CraiglistPropertyCrawlSpider(CrawlSpider):

    name = "Craigs-Property-Crawler"
    allowed_domains = ["https://craigslist.org"]
    start_urls = [
        # 'http://www.wimdu.com/great-britain?object_types%5B%5D=apartment&object_types%5B%5D=house&sort_by=score',
        'https://craigslist.org/search/ela?query=television&srchType=T&hasPic=1',
    ]

    def parse(self, response):
        yield Request('https://goldcountry.craigslist.org/ele/5624980765.html',callback=self.parse_item)
        next_page = response.xpath("//a[@class='button next']/@href")
        for url in next_page.extract():
            yield Request(urlparse.urljoin('https://auburn.craigslist.org', url))

        propertiesLinks = response.xpath("//a[@class='hdrlnk']/@href")
        for url in propertiesLinks.extract():
            # print "------"
            # print urlparse.urljoin('https://www.9flats.com', url)
            yield Request(urlparse.urljoin('https://craigslist.org', url), callback=self.parse_item)



    def cleanUrl(self , url):
        return re.match(r'(.*)\((.*)\)(.*)', url).group(2).replace('small','large')

    def parse_item(self, response):
        # print "....................."
        l = ItemLoader(item=PropertyCrawlerItem(), response=response)
        l.add_xpath('imageUrl', "//div[@class='thumb']/@style", MapCompose(lambda i : re.match(r'(.*)\((.*)\)(.*)', i).group(2).replace('small','large')))
        l.add_value('propertyUrl', response.url)
        l.add_xpath('propertyName', "//span[@class='postingtitletext']/text()", MapCompose(unicode.strip))
        l.add_xpath('price', "//span[@class='postingtitletext']/text()", MapCompose(unicode.strip))
        return l.load_item()

process = CrawlerProcess({
     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    })
process.crawl(CraiglistPropertyCrawlSpider)

process.start()


