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


class FlatsPropertyCrawlSpider(CrawlSpider):

    name = "Flats-Property-Crawler"
    allowed_domains = ["www.9flats.com"]
    start_urls = [
        # 'http://www.wimdu.com/great-britain?object_types%5B%5D=apartment&object_types%5B%5D=house&sort_by=score',
        'https://www.9flats.com/searches?utf8=%E2%9C%93&mode=list&search%5Bcurrency%5D=EUR&search%5Bsort_by%5D=top_ranking&search%5Bradius%5D=25&search%5Bwoeid%5D=24554868&search%5Blat%5D=52.019&search%5Blng%5D=-1.97406&search%5Bgeo_region%5D=false&search%5Bpoint_of_interest%5D=false&search%5Bstart_date_alt%5D=2016-05-27&search%5Bend_date_alt%5D=2016-05-28&search%5Bquery%5D=England%2C+United+Kingdom&search%5Bstart_date%5D=&search%5Bend_date%5D=&search%5Bnumber_of_beds%5D=2&number_of_adults=2&search%5Bnumber_of_children%5D=0&commit=Search',
    ]

    def parse(self, response):
        propertiesLinks = response.xpath("//a[@class='search__place__content__title']/@href")
        for url in propertiesLinks.extract():
            print "------"
            print urlparse.urljoin('https://www.9flats.com', url)
            yield Request(urlparse.urljoin('https://www.9flats.com', url), callback=self.parse_item)
            # request.meta['property_link'] = link.split("?")[0]
            # print "................"
            # print urlparse.urljoin("https://www.9flats.com", link.split("?")[0])
            # yield request
    def cleanUrl(self , url):
        return re.match(r'(.*)\((.*)\)(.*)', url).group(2).replace('small','large')

    def parse_item(self, response):
        print "....................."
        l = ItemLoader(item=PropertyCrawlerItem(), response=response)
        l.add_xpath('imageUrl', "//div[@class='place__gallery__thumb']/@style", MapCompose(lambda i : re.match(r'(.*)\((.*)\)(.*)', i).group(2).replace('small','large')))
        l.add_value('propertyUrl', response.url)
        return l.load_item()



process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
})

process.crawl(FlatsPropertyCrawlSpider)

process.start()


