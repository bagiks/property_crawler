
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import re
import urlparse
from scrapy.loader import ItemLoader


from property_crawler.items import ImageItems

class GumtreeImageCrawlSpider(CrawlSpider):
    name = "Gumtree-Image-Spider"
    allowed_domains = ["gumtree.com"]
    start_urls = [
        'https://www.gumtree.com/search?search_category=home-garden'
    ]

    # custom_settings = {
    #     'ITEM_PIPELINES' :{'property_crawler.pipelines.MongoImagePipeline': 1},
    #     'IMAGES_STORE':'./images/gumtree'
    # }

    def parse(self, response):
        next_page = response.xpath("//li[@class='pagination-next']//a/@href")
        for url in next_page.extract():
            yield Request(urlparse.urljoin('https://gumtree.com', url))

        propertiesLinks = response.xpath("//a[@class='listing-link']/@href")
        for url in propertiesLinks.extract():
            if len(url) > 0:
                print "------"
                print urlparse.urljoin('https://gumtree.com', url)
                request = Request(urlparse.urljoin('https://gumtree.com', url), callback=self.parse_image_page)
                request.meta['directory'] = url
                yield request

    def parse_image_page(self, response):
        image_urls = response.xpath("//div[@id='vip-tabs-images']//li//img[@itemprop='image']/@src")
        l = ItemLoader(item=ImageItems(), response=response)
        items = []
        for url in image_urls.extract():
            if "jpg" in url or "JPG" in url:
                item = ImageItems()
                item['image_urls'] = [url]
                item['directory'] = response.meta['directory']
                item['image_name'] = url
                items.append(item)

        image_urls = response.xpath("//div[@id='vip-tabs-images']//li//img[@itemprop='image']/@data-lazy")
        l = ItemLoader(item=ImageItems(), response=response)
        items = []
        for url in image_urls.extract():
            if "jpg" in url or "JPG" in url:
                item = ImageItems()
                item['image_urls'] = [url]
                item['directory'] = response.meta['directory']
                item['image_name'] = url
                items.append(item)
        return items

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# })
#
# process.crawl(GumtreeImageCrawlSpider)
#
# process.start()