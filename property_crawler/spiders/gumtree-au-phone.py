from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import re
import urlparse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
import hashlib

from scrapy.utils.python import to_bytes

from property_crawler.items import PropertyImageItems


class GumtreeAuImageCrawlSpider(CrawlSpider):
    name = "Gumtree-Au-Image-Spider"
    rotate_user_agent = True
    allowed_domains = ["www.gumtree.com.au"]
    start_urls = [
        # "http://www.gumtree.com.au/s-sofas/c20079"
        #	'http://www.gumtree.com.au/s-blenders-juicers-food-processors/c21002',
        # 'http://www.gumtree.com.au/s-coffee-machines/c21000',
        # 'http://www.gumtree.com.au/s-cooktops-rangehoods/c20059',
        # 'http://www.gumtree.com.au/s-dishwashers/c20060',
        # 'http://www.gumtree.com.au/s-ovens/c20063',
        # 'http://www.gumtree.com.au/s-vacuum-cleaners/c20065',
        # 'http://www.gumtree.com.au/s-washing-machines-dryers/c20066'
        # 'http://www.gumtree.com.au/s-air-conditioning-heating/c20062',
        # 'http://www.gumtree.com.au/s-sewing-machines/c21001',
        # 'http://www.gumtree.com.au/s-small-appliances/c20064',
        # 'http://www.gumtree.com.au/s-fridges-freezers/c20061'
        # 'http://www.gumtree.com.au/s-other-appliances/c18402'


        # extra
        #	'http://www.gumtree.com.au/s-tv-dvd-players/c21127'
        #	'http://www.gumtree.com.au/s-lighting/c21027'
        # 'http://gumtree.com.au/s-laptops/c18553',
        # 'http://gumtree.com.au/s-computer-accessories/c18554',
        # 'http://gumtree.com.au/s-desktops/c18551',
        # 'http://gumtree.com.au/s-printers-scanners/c18555',
        # 'http://gumtree.com.au/s-modems-routers/c21110',
        # 'http://gumtree.com.au/s-monitors/c21111',
        #	'http://gumtree.com.au/s-other-computers-software/c18558',
        # 'http://www.gumtree.com.au/s-computer-speakers/c18557'
        'https://www.gumtree.com.au/s-other-phones/c18600'
    ]
    price_types = ["fixed", "negotiable", "free"]

    # category = "sofa"
    # category_code = "c20079"
    # places = {
    #     "act": "3008838",
    #     "nsw": "3008839",
    #     "nt": "3008840",
    #     "qld": "3008841",
    #     "sa": "3008842",
    #     "tas":"3008843",
    #     "vic":"3008844",
    #     "wa":"3008845"
    # }

    custom_settings = {
        'ITEM_PIPELINES': {
            'property_crawler.pipelines.MongoDBPipeline': 102,
            'scrapy.pipelines.images.ImagesPipeline': 101
        },

        # # S3 production
        # 'IMAGES_STORE' : "s3://3giks-property/gumtree-au/",
        #
        # # S3 test
        # 'IMAGES_STORE': "s3://3giks-property/gumtree-au/test/",

        # test
        "IMAGES_STORE": 'images/'

    }

    def parse(self, response):
        location_urls = response.xpath("//div[@class='refine-search-filter'][h3='Places']//a/@href")
        for location_url in location_urls.extract():
            for price_type in self.price_types:
                full_url = location_url + "?price-type=" + price_type
                yield Request(urlparse.urljoin('http://www.gumtree.com.au', full_url), callback=self.parse_item_list)

    def parse_item_list(self, response):
        next_pages = response.xpath("//a[@class='paginator__button paginator__button-next']//@href")
        for next_page in next_pages.extract():
            yield Request(urlparse.urljoin('http://www.gumtree.com.au', next_page), callback=self.parse_item_list)

        yield self.parse_item(response)

    def parse_item(self, response):
        l = ItemLoader(item=PropertyImageItems(), response=response)
        image_urls = \
            response.xpath(
                "//div[@itemprop='offers']/div[@class='ad-listing__thumb-container   ad-listing__thumb--loading ']"
                "/a[@itemprop='url']//img/@src").extract()
        l.add_value('image_urls', map(self.extract_img_url, image_urls))
        return l.load_item()

    def replaceNonBreakingSpace(self, x):
        return x.replace(u'\xa0', " ")

    def extract_img_url(self, x):
        return x.split('$_')[0] + "$_10.jpg"


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
})

process.crawl(GumtreeAuImageCrawlSpider)

process.start()
