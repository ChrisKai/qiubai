# -*- coding: utf-8 -*-

import logging
import pymongo
from settings import MONGO_HOST, MONGO_PORT
from items import EmbarrassingIndexItem, PersonalInformationItem, FollowsItem, FansEachItem, FansItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QiubaiPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = client['qiubai']
        self.embarrassing_index = db['embarrassing_index']
        self.personal_information = db['personal_information']
        self.follows = db['follows']
        self.fans_each = db['fans_each']
        self.fans = db['fans']
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        """ Judge items type, and store it into mongo"""
        if isinstance(item, EmbarrassingIndexItem):
            try:
                self.embarrassing_index.insert(dict(item))
            except Exception as e:
                self.logger.info('糗百指数存储失败：' + str(e))
        elif isinstance(item, PersonalInformationItem):
            try:
                self.personal_information.insert(dict(item))
            except Exception as e:
                self.logger.info('个人信息存储失败：' + str(e))
        elif isinstance(item, FollowsItem):
            follow_items = dict(item)
            follows = follow_items.pop("follows")
            for i in range(len(follows)):
                follow_items[str(i + 1)] = follows[i]
            try:
                self.follows.insert(follow_items)
            except Exception as e:
                self.logger.info('关注人存储失败：' + str(e))
        elif isinstance(item, FansEachItem):
            fan_each_items = dict(item)
            follows = fan_each_items.pop("fans_each")
            for i in range(len(follows)):
                fan_each_items[str(i + 1)] = follows[i]
            try:
                self.fans_each.insert(fan_each_items)
            except Exception as e:
                self.logger.info('互粉好友存储失败：' + str(e))
        elif isinstance(item, FansItem):
            fan_items = dict(item)
            fans = fan_items.pop('fans')
            for i in range(len(fans)):
                fan_items[str(i + 1)] = fans[i]
            try:
                self.fans.insert(fan_items)
            except Exception as e:
                self.logger.info('好友id存储失败：' + str(e))
        return item
