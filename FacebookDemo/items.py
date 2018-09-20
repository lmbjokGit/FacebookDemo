# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class ProductItem(Item):
    comment = Field()
    like1 = Field()
    like2 = Field()
    likes = Field()
    sitename = Field()
    sitelikes = Field()
    sitelooks = Field()
    seq = Field()
