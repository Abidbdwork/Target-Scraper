# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TargetItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    highlights = scrapy.Field()
    specifications = scrapy.Field()
    questions = scrapy.Field()
