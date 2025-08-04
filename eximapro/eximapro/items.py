# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RostenderItem(scrapy.Item):
    tender_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    date_start = scrapy.Field()
    date_end = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    categories = scrapy.Field()
