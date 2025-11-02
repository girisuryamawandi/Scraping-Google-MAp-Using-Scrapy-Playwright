# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlaywrightScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    google_map_link = scrapy.Field()
    name = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field() 