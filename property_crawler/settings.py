# -*- coding: utf-8 -*-

# Scrapy settings for property_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'property_crawler'

SPIDER_MODULES = ['property_crawler.spiders']
NEWSPIDER_MODULE = 'property_crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'property_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'property_crawler.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'property_crawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "bagiks"
MONGODB_COLLECTION = "property"
MONGODB_URI = 'mongodb://localhost:27017'
# ITEM_PIPELINES = {'property_crawler.pipelines.MongoDBPipeline':100}
#ITEM_PIPELINES = {'property_crawler.pipelines.MongoImagePipeline': 1}
# IMAGES_STORE ='./images/gumtree.au'
# Retry many times since proxies often fail
RETRY_TIMES = 5
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    'property_crawler.middlewares.IgnoreDuplicatesMiddleware': 80,

    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # Fix path to this module
    #'property_crawler.rotateproxymiddlewares.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # change proxy
    'property_crawler.middlewares.RotateUserAgentMiddleware': 120,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
}

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
PROXY_LIST = 'list.txt'
# ITEM_PIPELINES = {
#     'property_crawler.pipelines.MongoDBPipeline':100,
#     'scrapy.pipelines.images.ImagesPipeline': 1
# }
#
# # ITEM_PIPELINES ={'scrapy.pipelines.images.ImagesPipeline': 1}
# IMAGES_STORE='images/sofa'

# ITEM_PIPELINES = [
#   'scrapy_mongodb.MongoDBPipeline',
# ]
#
# MONGODB_URI = 'mongodb://localhost:27017'
# MONGODB_DATABASE = 'bagiks'
# MONGODB_COLLECTION = 'properties'
#
# MONGODB_UNIQUE_KEY = 'propertyUrl'


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


#DOWNLOAD_TIMEOUT=5000

#USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

USER_AGENT_CHOICES = [
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    # New user agents from http://whatsmyuseragent.com/commonuseragents
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; like Gecko',
    'Mozilla/5.0 ;iPhone; CPU iPhone OS 8_1_2 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12B440 Safari/600.1.4',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 ;Windows NT 6.3; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 ;Windows NT 6.1; rv:34.0; Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; rv:34.0; Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 ;compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0;',
    'Mozilla/5.0 ;Windows NT 6.2; WOW64; rv:27.0; Gecko/20100101 Firefox/27.0',
    'Mozilla/5.0 ;compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html;',
    'Mozilla/5.0 ;Windows NT 6.3; WOW64; Trident/7.0; rv:11.0; like Gecko',
    'Mozilla/5.0 ;iPhone; CPU iPhone OS 7_1_2 like Mac OS X; AppleWebKit/537.51.2 ;KHTML, like Gecko; Version/7.0 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 ;Windows NT 6.1; rv:35.0; Gecko/20100101 Firefox/35.0',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; rv:35.0; Gecko/20100101 Firefox/35.0',
    'Mozilla/5.0 ;Windows NT 6.3; WOW64; rv:34.0; Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 ;iPad; CPU OS 8_1_2 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12B440 Safari/600.1.4',
    'Mozilla/5.0 ;Windows NT 6.1; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 ;Macintosh; Intel Mac OS X 10_10_1; AppleWebKit/600.2.5 ;KHTML, like Gecko; Version/8.0.2 Safari/600.2.5',
    'Mozilla/5.0 ;Windows NT 6.3; WOW64; rv:35.0; Gecko/20100101 Firefox/35.0',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.99 Safari/537.36',
    'Mozilla/5.0 ;Macintosh; Intel Mac OS X 10_10_1; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 ;iPhone; CPU iPhone OS 8_0_2 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12A405 Safari/600.1.4',
    'Mozilla/5.0 ;Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/40.0.2214.93 Safari/537.36',
    'Mozilla/5.0 ;Windows NT 5.1; rv:34.0; Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 ;Windows NT 5.1; rv:35.0; Gecko/20100101 Firefox/35.0'
]
