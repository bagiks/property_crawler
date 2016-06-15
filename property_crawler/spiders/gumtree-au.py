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

class GumtreeBedImageCrawlSpider(CrawlSpider):
    name = "Gumtree-Au-Image-Spider-Bed"
    rotate_user_agent = True
    allowed_domains = ["www.gumtree.com.au"]
    start_urls = [
        "http://www.gumtree.com.au/s-sofas/c20079"
    ]
    category = "sofa"

    category_name = "s-sofas"
    category_code = "c20079"
    price_types = ["fixed", "negotiable", "free"]
    places = {
        "act": "3008838",
        "nsw": "3008839",
        "nt": "3008840",
        "qld": "3008841",
        "sa": "3008842",
        "tas":"3008843",
        "vic":"3008844",
        "wa":"3008845"
    }

    custom_settings = {
        'ITEM_PIPELINES': {'property_crawler.pipelines.MongoImagePipeline': 1},
        'IMAGES_STORE':'./images/sofa'
    }

    # def __int__(self):
    #     #http://www.gumtree.com.au/s-sofas/act/c20079l3008838?price-type=negotiable
    #     for key, value in self.places.iteritems():
    #         for price_type in self.price_types:
    #             url = "http://"+self.allowed_domains[0]+"/"+self.category_name+"/"+key+"/"+self.category_name+"l"+self.category_code
    #             +"?price_type="+price_type
    #             print url
    #             self.start_urls.extend(url)

    def parse(self, response):
        location_urls = response.xpath("//div[@class='refine-search-filter'][h3='Places']//a/@href")
        for location_url in location_urls.extract():
            for price_type in self.price_types:
                full_url = location_url+"?price-type="+price_type
                yield Request(urlparse.urljoin('http://www.gumtree.com.au',full_url), callback=self.parse_page_list)

    def parse_page_list(self, response):
        next_pages = response.xpath("//a[@class='rs-paginator-btn next']//@href")
        for next_page in next_pages.extract():
            yield Request(urlparse.urljoin('http://www.gumtree.com.au',next_page), callback=self.parse_page_list)

        item_urls = response.xpath("//div[@class='rs-ad-field rs-ad-detail']/div/a[@itemprop='url']/@href")
        for item_url in item_urls.extract():
            # print item_url
            yield Request(urlparse.urljoin('http://www.gumtree.com.au',item_url), callback=self.parse_item)

    def parse_item(self, response):
        l = ItemLoader(item=PropertyImageItems(), response=response)

        l.add_xpath('title', "//h1[@id='ad-title']/text()", MapCompose(unicode.strip))
        l.add_xpath('price',"//div[@id='ad-price']//span[@class='j-original-price']/text()", MapCompose(unicode.strip))
        l.add_xpath('description',"//div[@id='ad-description']/text()", Join('\n'))
        header = response.xpath("//div[@id='breadcrumb']//li//text()").extract()
        l.add_value('item_id', header[-1].split(u'\xa0')[-1])
        l.add_value('tags',header[1:-1])

        image_urls = response.xpath("//div[@class='carousel-wrap ad-gallery-thumbs']//span/@data-src").extract()
        l.add_value('image_urls',map(lambda x: x.replace("$_74.","$_10."), image_urls))
        l.add_value('category', self.category)
        l.add_value('source', self.allowed_domains[0])
        l.add_value('page_id',hashlib.sha1(to_bytes(response.url)).hexdigest())

        return l.load_item()

    def replaceNonBreakingSpace(self,x):
        return x.replace(u'\xa0'," ")

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# })
#
# process.crawl(GumtreeBedImageCrawlSpider)
#
# process.start()