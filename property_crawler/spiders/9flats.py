# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.http import Request
import urlparse
import logging
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
        'https://www.9flats.com/searches?commit=Search&mode=list&number_of_adults=2&random=1464390500315&search[amenities]=&search[category]=&search[currency]=EUR&search[end_date]=&search[geo_region]=false&search[language]=en&search[lat]=55.3781&search[lng]=-3.43597&search[number_of_bathrooms]=&search[number_of_bedrooms]=&search[number_of_beds]=2&search[number_of_children]=0&search[page]=1&search[place_type]=&search[point_of_interest]=false&search[query]=United+Kingdom,+Europe&search[radius]=25&search[sort_by]=top_ranking&search[start_date]=&search[woeid]=23424975&timestamp=1464390500315',
    ]

    def parse(self, response):

        next_page = response.xpath("//a[@class='pagination__item__link pagination__item__link_next']/@href")
        for url in next_page.extract():
            yield Request(urlparse.urljoin('https://www.9flats.com', url))

        propertiesLinks = response.xpath("//a[@class='search__place__content__title']/@href")
        for url in propertiesLinks.extract():
            # print "------"
            # print urlparse.urljoin('https://www.9flats.com', url)
            yield Request(urlparse.urljoin('https://www.9flats.com', url), callback=self.parse_item)



    def cleanUrl(self , url):
        return re.match(r'(.*)\((.*)\)(.*)', url).group(2).replace('small','large')

    def parse_item(self, response):
        # print "....................."
        l = ItemLoader(item=PropertyCrawlerItem(), response=response)
        l.add_xpath('imageUrl', "//div[@class='place__gallery__thumb']/@style", MapCompose(lambda i : re.match(r'(.*)\((.*)\)(.*)', i).group(2).replace('small','large')))
        l.add_value('propertyUrl', response.url)
        l.add_xpath('propertyName', "//h1[@class='place__header__title']/text()", MapCompose(unicode.strip))
        return l.load_item()

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# })
#
# process.crawl(FlatsPropertyCrawlSpider)
#
# process.start()


