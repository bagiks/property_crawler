
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import re
import urlparse
from scrapy.loader import ItemLoader
from randomproxy import RandomProxy
from scrapy.conf import settings

from property_crawler.items import ImageItems

class IndoorImageCrawlSpider(CrawlSpider):
    name = "Indoor-Image-Spider"
    allowed_domains = ["people.csail.mit.edu"]
    start_urls = [
        'http://people.csail.mit.edu/brussell/research/LabelMe/Images/'
    ]
    custom_settings = {
        'ITEM_PIPELINES' :{'scrapy.pipelines.images.ImagesPipeline': 1},
        'IMAGES_STORE':'./images'
    }

    randomProxy = RandomProxy(settings)

    def parse(self, response):
        image_directory_urls = response.xpath("//a/@href")
        for url in image_directory_urls.extract():
            if "indoor" in str(url).lower():
                request = Request(urlparse.urljoin(self.start_urls[0],url), callback=self.parse_image_page)
                request.meta['directory'] = url
                self.randomProxy.process_request(request,self)
                yield request


    def parse_image_page(self, response):
        image_urls = response.xpath("//a/@href")
        # l = ItemLoader(item=ImageItems(), response=response)
        items = []
        for url in image_urls.extract():
            if "jpg" in url:
                item = ImageItems()
                item['image_urls'] = [urlparse.urljoin(response.url, url)]
                item['directory'] = response.meta['directory']
                item['image_name'] = url
                items.append(item)
        return items

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
})

process.crawl(IndoorImageCrawlSpider)

process.start()