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
        # 'sofa'
        'http://www.gumtree.com.au/s-sofas/c20079',
        # 'bed'
        'http://www.gumtree.com.au/s-beds/c20074',
        # 'monitor'
        'http://www.gumtree.com.au/s-monitors/c21111',
        # 'washing machine'
        'http://www.gumtree.com.au/s-washing-machines-dryers/washing+machine/k0c20066',
        # 'microwave'
        'http://www.gumtree.com.au/s-microwaves/c21003',
        # 'printer',
        'http://www.gumtree.com.au/s-printers-scanners/c18555',
        # 'speaker',
        'http://www.gumtree.com.au/s-speakers/c21102',
        # 'table',
        'http://www.gumtree.com.au/s-dining-tables/table/k0c20080',
        # 'bicycle',
        'http://www.gumtree.com.au/s-bicycles/bike/k0c18560',

        # 'dishwasher',
        'http://www.gumtree.com.au/s-dishwashers/c20060',

        # 'computer',
        'http://www.gumtree.com.au/s-desktops/c18551',

        # laptop,
        'http://www.gumtree.com.au/s-laptops/c18553',

        # 'drawer',
        'http://www.gumtree.com.au/s-dressers-drawers/c21015',

        # 'suitcase',
        'http://www.gumtree.com.au/s-suitcase+wheels/k0',
        # 'refrigerator',
        'http://www.gumtree.com.au/s-fridges-freezers/k0c20061',
        # 'chair',
        'http://www.gumtree.com.au/s-armchairs/c21005',
        # 'mirror',
        'http://www.gumtree.com.au/s-mirrors/c20077',
        # 'sideboard',
        'http://www.gumtree.com.au/s-buffets-side-tables/side+board/k0c21011',
        # 'vacuum',
        'http://www.gumtree.com.au/s-vacuum-cleaners/c20065',
        # 'heater',
        'http://www.gumtree.com.au/s-air-conditioning-heating/heater/k0c20062',
        # 'desk',
        'http://www.gumtree.com.au/s-desks/desk/k0c20076',
        # 'tv',
        'http://www.gumtree.com.au/s-entertainment-tv-units/television/k0c21012',
        # 'wardrobe',
        'http://www.gumtree.com.au/s-wardrobes/c20081',
        # 'lamp',
        'http://www.gumtree.com.au/s-table-desk-lamps/lamp/k0c21026',
        # 'bookshelf',
        'http://www.gumtree.com.au/s-bookcases-shelves/bookshelf/k0c21013',
        # piano',
        'http://www.gumtree.com.au/s-keyboards-pianos/piano/k0c18609',
        # 'cooker',
        'http://www.gumtree.com.au/s-rice+cooker/k0'
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
            'property_crawler.pipelines.MongoDBPipeline':102,
            'scrapy.pipelines.images.ImagesPipeline': 101,
            'property_crawler.pipelines.DynamicPathImgPipeline': 103,
        },

        # # S3 production
        # 'IMAGES_STORE' : "s3://3giks-property/gumtree-au/",
        #
        # # S3 test
        # 'IMAGES_STORE': "s3://3giks-property/gumtree-au/test/",

        # test
        "IMAGES_STORE" :'images/'

    }

    def parse(self, response):
        location_urls = response.xpath("//div[@class='refine-search-filter'][h3='Places']//a/@href")
        for location_url in location_urls.extract():
            for price_type in self.price_types:
                full_url = location_url+"?price-type="+price_type
                yield Request(urlparse.urljoin('http://www.gumtree.com.au', full_url), callback=self.parse_page_list)

    def parse_page_list(self, response):
        next_pages = response.xpath("//a[@class='paginator__button paginator__button-next']//@href")

        for next_page in next_pages.extract():
            if "page-2" not in next_page:
                yield Request(urlparse.urljoin('http://www.gumtree.com.au', next_page), callback=self.parse_page_list)

        item_urls = response.xpath("//div[@itemprop='offers']/div/a[@itemprop='url']/@href")
        for item_url in item_urls.extract():
            # print item_url
            yield Request(urlparse.urljoin('http://www.gumtree.com.au', item_url), callback=self.parse_item)

    def parse_item(self, response):
        l = ItemLoader(item=PropertyImageItems(), response=response)

        l.add_xpath('title', "//h1[@id='ad-title']/text()", MapCompose(unicode.strip))
        l.add_xpath('price',"//div[@id='ad-price']//span[@class='j-original-price']/text()", MapCompose(unicode.strip))
        l.add_xpath('description',"//div[@class='ad-details__ad-description-details']/text()", Join('\n'))
        header = response.xpath("//div[@id='breadcrumb']//li//text()").extract()
        l.add_value('item_id', header[-1].split(u'\xa0')[-1])
        l.add_value('tags',header[1:-1])

        image_urls = response.xpath("//div[@class='gallery-thumbs']//span/@data-responsive-image").extract()

        l.add_value('image_urls', map(self.extract_img_url, image_urls[-2:]))
        l.add_value('category', header[-2])
        l.add_value('source', self.allowed_domains[0])
        l.add_value('page_id',hashlib.sha1(to_bytes(response.url)).hexdigest())

        l.add_value('page_url', response.url)

        return l.load_item()

    def replaceNonBreakingSpace(self, x):
        return x.replace(u'\xa0'," ")

    def extract_img_url(self, x):
        try:
            m = re.search('(?<=large):\'(.*)\'}(.*)', x)
            return m.group(1)
        except AttributeError, TypeError:
            print("Cannot extract from " + x)

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# })
#
# process.crawl(GumtreeAuImageCrawlSpider)
#
# process.start()


