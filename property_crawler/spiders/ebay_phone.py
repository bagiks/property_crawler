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


class EbayImageCrawlSpider(CrawlSpider):
    name = "Ebay-phone-Spider"
    rotate_user_agent = True
    allowed_domains = ["www.ebay.com"]
    start_urls = [
        'http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_ItemCondition=3000&_nkw=smartphone&_pgn=1&_skc=450&rt=nc'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'property_crawler.pipelines.MongoDBPipeline': 99,
            'scrapy.pipelines.images.ImagesPipeline': 101
        },

        # test
        "IMAGES_STORE": 'images/'

    }

    def parse(self, response):
        next_pages = response.xpath("//td[@class='pagn-next']/a[@class='gspr next']/@href")
        for next_page in next_pages.extract():
            yield Request(next_page, callback=self.parse)

        item_urls =  response.xpath("//div[@class='lvpicinner full-width picW']/a[@class='img imgWr2']/@href")
        for item_url in item_urls.extract():
            # print item_url
            yield Request(item_url, callback=self.parse_item)

    def parse_item(self, response):
        l = ItemLoader(item=PropertyImageItems(), response=response)

        l.add_xpath('title', "//h1[@id='itemTitle']/text()", MapCompose(unicode.strip))

        image_urls = response.xpath("//td[@class='tdThumb']/div/img/@src").extract()

        l.add_value('image_urls', map(self.extract_img_url, image_urls))

        l.add_value('page_url', response.url)

        return l.load_item()
        pass

    def replaceNonBreakingSpace(self, x):
        return x.replace(u'\xa0', " ")

    # http://i.ebayimg.com/images/g/6qcAAOSwr7ZW2iJv/s-l64.jpg
    def extract_img_url(self, x):
        return x.split("s-l")[0] + "s-l1600.jpg"

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# })
#
# process.crawl(EbayImageCrawlSpider)
#
# process.start()
