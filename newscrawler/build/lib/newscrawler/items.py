# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    cid = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    title_jp = scrapy.Field()
    content_jp =  scrapy.Field()
    grade = scrapy.Field()
    sort = scrapy.Field()
    created_at = scrapy.Field()
    up_counts = scrapy.Field()
    down_counts = scrapy.Field()
    zan_status = scrapy.Field()
    pass
