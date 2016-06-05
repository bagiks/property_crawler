Installation
===========
1. Install Anaconda, python 2.7

2. Creat a new enviroment `scraping` with scrapy package

```
	conda create --name scraping Scrapy
```
3. Activate / deactivate the enviroment
``` 
	source actiavate scraping
```
```
	source deactivate
```
4. Clone `property_crawler` repository
```
	https://github.com/bagiks/property_crawler
	cd property_crawler
```
5. Install python package
```
	pip install -r requirements.txt
```
6. Install mongodb and start service
7. Create db `bagiks`, collection `property`
8. Run 
	``` scrapy crawl Flats-Property-Crawler``

---
9. Dev with Pycharm
- Change Python Interpreter to `scraping` enviroment
[https://www.jetbrains.com/help/pycharm/2016.1/configuring-python-interpreter-for-a-project.html]
- Go to `property_crawler/spiders/9flats.py`, uncomment this block
```python
process = CrawlerProcess({
     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
 })

process.crawl(FlatsPropertyCrawlSpider)

process.start()
```
- Run 9flats.py 
