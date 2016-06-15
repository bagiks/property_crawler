from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import re
import urlparse
from scrapy.loader import ItemLoader


from property_crawler.items import PropertyImageItems


class GumtreeBedImageCrawlSpider(CrawlSpider):
    name = "GumtreeImageSpiderBed"
    allowed_domains = ["www.gumtree.com.au"]
    start_urls = [
        "http://www.gumtree.com.au/s-sofas/c20079"
    ]

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

    # custom_settings = {
    #     'ITEM_PIPELINES' :{'property_crawler.pipelines.MongoImagePipeline': 1},
    #     'IMAGES_STORE':'./images/gumtree'
    # }

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

        l.add_xpath('title', "//h1[@id='ad-title']/text()")
        l.add_xpath('price',"//div[@id='ad-price']//span[@class='j-original-price']/text()")
        l.add_xpath('description',"//div[@id='ad-description']/text()")
        header = response.xpath("//div[@id='breadcrumb']//li//text()").extract()
        l.add_value('id', header[-1].split(u'\xa0')[-1])
        l.add_value('tag',header[1:-1])

        image_urls = response.xpath("//div[@class='carousel-wrap ad-gallery-thumbs']//span/@data-src").extract()
        l.add_value('image_urls',map(lambda x: x.replace("$_74.","$_10."), image_urls))

        return l.load_item()




    # def parse(self, response):
    #     next_page = response.xpath("//li[@class='pagination-next']//a/@href")
    #     for url in next_page.extract():
    #         yield Request(urlparse.urljoin('https://gumtree.com', url))
    #
    #     propertiesLinks = response.xpath("//a[@class='listing-link']/@href")
    #     for url in propertiesLinks.extract():
    #         if len(url) > 0:
    #             print "------"
    #             print urlparse.urljoin('https://gumtree.com', url)
    #             request = Request(urlparse.urljoin('https://gumtree.com', url), callback=self.parse_image_page)
    #             request.meta['directory'] = url
    #             yield request

    # def parse_image_page(self, response):
    #     image_urls = response.xpath("//div[@id='vip-tabs-images']//li//img[@itemprop='image']/@src")
    #     items = []
    #     for url in image_urls.extract():
    #         if "jpg" in url or "JPG" in url:
    #             item = ImageItems()
    #             item['image_urls'] = [url]
    #             item['directory'] = response.meta['directory']
    #             item['image_name'] = url
    #             items.append(item)
    #
    #     image_urls = response.xpath("//div[@id='vip-tabs-images']//li//img[@itemprop='image']/@data-lazy")
    #     l = ItemLoader(item=ImageItems(), response=response)
    #     items = []
    #     for url in image_urls.extract():
    #         if "jpg" in url or "JPG" in url:
    #             item = ImageItems()
    #             item['image_urls'] = [url]
    #             item['directory'] = response.meta['directory']
    #             item['image_name'] = url
    #             items.append(item)
    #     return items

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# })
#
# process.crawl(GumtreeBedImageCrawlSpider)
#
# process.start()