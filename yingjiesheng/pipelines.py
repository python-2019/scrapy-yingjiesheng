# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json

from pymongo import MongoClient
from scrapy.conf import settings


class YingjieshengPipeline(object):

    def open_spider(self, spider):
        # self.file = None
        # 存储方式
        self.method = settings.get("WRITE_METHOD")
        print("你使用的存储方式: "+ self.method)
        # 初始化 csv
        if (self.method == "csv" or self.method is None):
            self.init_csv()
        # 初始化 mongo
        elif (self.method == "mongo"):
            self.init_mongo_db()

    def process_item(self, item, spider):
        post_list = item['post']
        # 判断是否中文
        for post in post_list:
            if '\u4e00' <= post <= '\u9fff':
                item['post'] = post
                break
        # 写入 csv
        if (self.method == "csv"):
            row = [item['post'], item['city'], item['date'], item['href']]
            self.write_csv(row)
            print(row)
        # 写入mongo
        elif (self.method == "mongo"):
            item_json = json.dumps(dict(item), ensure_ascii=False)
            self.write_mongo(dict(item))
            print(item_json)
        return item

    def close_spider(self, spider):
        if hasattr(YingjieshengPipeline, 'file'):
            self.file.flush()

    def write_csv(self, arr):
        """
        写入到 csv
        :param arr:
        :return:
        """
        self.csv_writer.writerow(arr)

    def write_mongo(self, json_str):

        """
        写入到 csv
        :param json_str: json 数据格式
        """
        self.collection.insert(json_str)

    def init_csv(self):

        """
            初始化 csv文件系统
        """
        self.file_path = settings.get("FILE_PATH")
        self.file = open(self.file_path, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.file)
        headers = ['职位', '城市', '发布时间', '详情链接']
        self.csv_writer.writerow(headers)

    def init_mongo_db(self):
        """
        初始化mongo db对象
        """
        # host
        host = settings.get("MONGO_HOST")
        # post
        port = settings.get("MONGO_PORT")
        # db name
        db_name = settings.get("MONGO_DB_NAME")
        # collection name
        collection_name = settings.get("MONGO_COLLECTION_NAME")
        self.mongo_client = MongoClient(host, port)
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]
