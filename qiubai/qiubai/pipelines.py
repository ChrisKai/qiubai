# -*- coding: utf-8 -*-

import pymongo
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
        client = pymongo.MongoClient("localhost", 27017)
        db = client["qiubai"]
        self.embarrassing_index = db["embarrassing_index"]
        self.personal_information = db["personal_information"]
        self.follows = db["follows"]
        self.fans_each = db["fans_each"]
        self.fans = db["fans"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, EmbarrassingIndexItem):
            try:
                self.embarrassing_index.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, PersonalInformationItem):
            try:
                self.personal_information.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, FollowsItem):
            follow_items = dict(item)
            follows = follow_items.pop("follows")
            for i in range(len(follows)):
                follow_items[str(i + 1)] = follows[i]
            try:
                self.follows.insert(follow_items)
            except Exception:
                pass
        elif isinstance(item, FansEachItem):
            fan_each_items = dict(item)
            follows = fan_each_items.pop("fans_each")
            for i in range(len(follows)):
                fan_each_items[str(i + 1)] = follows[i]
            try:
                self.fans_each.insert(fan_each_items)
            except Exception:
                pass
        elif isinstance(item, FansItem):
            fan_items = dict(item)
            fans = fan_items.pop("fans")
            for i in range(len(fans)):
                fan_items[str(i + 1)] = fans[i]
            try:
                self.fans.insert(fan_items)
            except Exception:
                pass
        return item