#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy
import time

import scrapy

# 这里是正确的 应该以spider上级目录为根目录
from yingjiesheng.items import YingjieshengItem


class yingjieshengScrapy(scrapy.Spider):
    """
        应届生求职网 爬虫
    """
    name = 'yingjiesheng'
    allowed_domains = ["yingjiesheng.com"]
    host = "http://www.yingjiesheng.com"
    start_urls = (
        host+"/commend-fulltime-1.html",
    )

    def parse(self, response):
        # 职位div list
        tr_list = response.xpath("//tr[@class='bg_0' or @class='bg_1']")
        # 遍历拉取信息
        for tr in tr_list:
            item = YingjieshengItem()
            item['city'] = tr.xpath("./td/a/span[@style='color: #008000;']/text()").extract_first()
            item['post'] = tr.xpath("./td/a/text()").extract()
            item['href'] = self.host+tr.xpath("./td/a/@href").extract_first()
            item['date'] = tr.xpath("./td[2]/text()").extract_first()
            yield item
        #  翻页
        next_page = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page is not None:
            next_page_url = self.host + next_page
            print("\n"+next_page_url+"\n")
            yield scrapy.Request(
                next_page_url,
                callback=self.parse
            )
