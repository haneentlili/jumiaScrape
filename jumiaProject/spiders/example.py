from __future__ import absolute_import
import scrapy

from jumiaProject.items import JumiaprojectItem

class ExampleSpider(scrapy.Spider):
    name = 'jumia'
    def __init__(self, category=None, *args, **kwargs):
        super(ExampleSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.jumia.com.tn/%s' % category]
    allowed_domains = ['jumia.com.tn']
    

    def parse(self, response):
        nextpage = response.xpath("//a[@title='Suivant']/@href")
        for item in self.scrape(response):
            yield item 
        if nextpage:
            path = nextpage.extract_first()
            nextpage = response.urljoin(path)
            yield scrapy.Request(nextpage, callback=self.parse)
    def scrape(self, response):
        ids=response.xpath("//div[contains(@class, '-gallery')]/@data-sku").extract()
        titles=response.xpath("//div[contains(@class, '-gallery')]//span[@class='name']/text()").extract()
        prices=response.xpath("//span[@class='price ']/span[1]/@data-price").extract()
        oldprices=response.xpath("//span[contains(@class,'price -old')]/span[1]/@data-price").extract()
        discounts=response.xpath("//div[contains(@class, '-gallery')]//span[@class='sale-flag-percent']/text()").extract()
        images=response.xpath("//div[contains(@class, '-gallery')]//img/@src").extract()
        prods = zip(ids,titles,discounts,images,prices,oldprices)
        for p in prods:
            item = JumiaprojectItem()
            item['_id'] =p[0] 
            item['title'] = p[1]
            item['price'] = p[4]
            item['oldprice'] = p[5]
            item['discount'] = p[2]
            item['image'] = p[3]
            yield item
