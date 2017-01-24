# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class QiubaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class EmbarrassingIndexItem(Item):
    """糗百指数"""
    _id = Field()  # 用户id
    num_fans = Field()  # 粉丝数
    num_follow = Field()  # 关注数
    embarrassing_things = Field()  # 糗事
    comments = Field()  # 评论
    smile_faces = Field()  # 笑脸


class PersonalInformationItem(Item):
    """个人资料"""
    _id = Field()  # 用户ID
    nick_name = Field()  # 用户昵称
    marriage = Field()  # 婚姻
    constellation = Field()  # 星座
    hometown = Field()  # 故乡
    profession = Field()  # 职业
    embarrassing_age = Field()  # 糗龄


class FollowsItem(Item):
    """关注人列表"""
    _id = Field()  # 用户id
    follows = Field()  # 关注


class FansItem(Item):
    """粉丝列表"""
    _id = Field()  # 用户id
    fans = Field()  # 粉丝


class FansEachItem(Item):
    """互粉好友"""
    _id = Field()  # 用户id
    fans_each = Field()  # 互粉好友