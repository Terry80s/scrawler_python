# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

###############################
#author:ChenRukun             #
#created:20180622             #
###############################

class NewscrawlerPipeline(object):

    def __init__(self):
        # connection = pymongo.Connection(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        #The pymongo api of new Client has changed after version 2.8
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        #print(pymongo.version)
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            #filter duplicate record->item['specify item']
            self.collection.update({'created_at':item['created_at']},dict(item),True)
            #self.collection.insert(dict(item))
            log.msg("lives added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
