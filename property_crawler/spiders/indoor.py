



from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import re
import urlparse
from scrapy.loader import ItemLoader


from property_crawler.items import ImageItems




class IndoorImageCrawlSpider(CrawlSpider):
    name = "Indoor-Image-Spider"
    allowed_domains = ["people.csail.mit.edu"]
    start_urls = [
        'http://people.csail.mit.edu/brussell/research/LabelMe/Images/'
    ]


    def parse(self, response):
        image_directory_urls = response.xpath("//a/@href")
        for url in image_directory_urls.extract():
            if "indoor" in str(url).lower():
                request = Request(urlparse.urljoin(self.start_urls[0],url), callback=self.parse_image_page)
                # request.meta['directory'] = url
                yield request


    def parse_image_page(self, response):
        image_urls = response.xpath("//a/@href")
        for url in image_urls.extract():
            if "jpg" in url:
                request = Request(urlparse.urljoin(response.url, url), callback=self.parse_item)
                # request.meta['directory'] = response.meta['directory']
                # request.meta['image_name'] = response.url
                print urlparse.urljoin(response.url, url)
                yield request

    def parse_item(self, response):
        l = ItemLoader(item=ImageItems(), response=response)
        l.add_value('image_urls', [str(response.url)])

        print '---------'
        # print response.meta['directory']
        # print response.meta['image_name']
        print response.url
        print '---------'
        # l.add_value('directory', response.meta['directory'])
        # l.add_value('image_name', response.meta['image_name'])

        return l.load_item()
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
})

process.crawl(IndoorImageCrawlSpider)

process.start()