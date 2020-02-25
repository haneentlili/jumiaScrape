import scrapy
class JumiaprojectItem(scrapy.Item):
    _id = scrapy.Field()
    price = scrapy.Field()
    oldprice = scrapy.Field()
    image = scrapy.Field()
    title = scrapy.Field()
    discount = scrapy.Field()
    category =  scrapy.Field()
