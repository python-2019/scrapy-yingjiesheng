# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YingjieshengItem(scrapy.Item):
    """
        应届生求职网抓取实体
    """
    # 职位
    post = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 链接
    href = scrapy.Field()
