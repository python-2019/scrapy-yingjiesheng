# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from scrapy.conf import settings


class YingjieshengPipeline(object):

    def open_spider(self, spider):
        file_path = settings.get("FILE_PATH")
        self.file = open(file_path, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.file)
        headers = ['职位', '城市', '发布时间', '详情链接']
        self.csv_writer.writerow(headers)

    def process_item(self, item, spider):
        post_list = item['post']
        post_ = ''
        for post in post_list:
            if '\u4e00' <= post <= '\u9fff':
                post_ = post
                break
        row = [post_, item['city'], item['date'], item['href']]
        self.csv_writer.writerow(row)
        print(row)
        return item

    def close_spider(self, spider):
        self.file.closed()
