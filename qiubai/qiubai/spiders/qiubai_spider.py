# -*- coding: utf-8 -*-
import re
import logging.config
from qiubai import settings
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.http import Request
from qiubai.ids import ids
from qiubai.items import EmbarrassingIndexItem, PersonalInformationItem, FollowsItem, FansItem, FansEachItem


class Spider(RedisSpider):
    name = "qiubai"
    allowed_domains = ["qiushibaike.com"]
    logging.config.dictConfig(settings.LOGGING)
    logger = logging.getLogger(__name__)

    def parse(self, response):
        pass

    def start_requests(self):
        for user_id in ids:
            yield Request(url="http://www.qiushibaike.com/users/{0}/".format(user_id), callback=self.parse_information)
            yield Request(url="http://www.qiushibaike.com/users/{0}/followers/".format(user_id),
                          callback=self.parse_follows_fans)

    @staticmethod
    def parse_information(response):
        selector = Selector(response)
        personal_information = PersonalInformationItem()  # 获取用户个人信息
        embarrassing_index = EmbarrassingIndexItem()  # 获取糗百指数列表
        if selector.xpath('//div[@class="user-block-header"]/h3[@class="comment"]/text()').extract()[0] != \
                u"当前用户已关闭糗百个人动态":
            data_need = selector.xpath('//div[@class="user-data-block"]').extract()
            personal_information_list = re.findall('.*?<span class="right">(.*?)</span>', data_need[1])  # 获取个人信息列表
            personal_information["nick_name"] = selector.xpath('//div[@class="user-header-name"]/h1/text()'
                                                               ).extract()[0]
            personal_information["_id"] = re.findall(".*?users/(.*?)/", response.url)[0]
            personal_information["marriage"] = personal_information_list[0]
            personal_information["constellation"] = personal_information_list[1]
            personal_information["hometown"] = personal_information_list[2]
            personal_information["profession"] = personal_information_list[3]
            personal_information["embarrassing_age"] = personal_information_list[4]

            embarrassing_index_list = re.findall('.*?<span class="right">(.*?)</span>', data_need[0])  # 获取糗百指数列表
            embarrassing_index["_id"] = re.findall(".*?users/(.*?)/", response.url)[0]
            embarrassing_index["num_fans"] = int(embarrassing_index_list[0])
            embarrassing_index["num_follow"] = int(embarrassing_index_list[1])
            embarrassing_index["embarrassing_things"] = int(embarrassing_index_list[2])
            embarrassing_index["comments"] = int(embarrassing_index_list[3])
            embarrassing_index["smile_faces"] = int(embarrassing_index_list[4])
        else:

            personal_information["_id"] = re.findall(".*?users/(.*?)/", response.url)[0]
            personal_information["marriage"] = None
            personal_information["constellation"] = None
            personal_information["hometown"] = None
            personal_information["profession"] = None
            personal_information["embarrassing_age"] = None

            embarrassing_index["_id"] = re.findall(".*?users/(.*?)/", response.url)[0]
            embarrassing_index["num_fans"] = None
            embarrassing_index["num_follow"] = None
            embarrassing_index["embarrassing_things"] = None
            embarrassing_index["comments"] = None
            embarrassing_index["smile_faces"] = None

        yield personal_information
        yield embarrassing_index

    def parse_follows_fans(self, response):
        selector = Selector(response)
        data_need = selector.xpath('//ul[@class="user-friends-block-list"]').extract()
        id_list = []
        follows_list = re.findall('.*?<a href="/users/(.*?)/" class="name">.*?', data_need[0])  # 获取关注人列表
        follow_items = FollowsItem()
        follow_items["_id"] = re.findall(".*?users/(.*?)/followers/", response.url)[0]
        follow_items["follows"] = follows_list
        id_list.extend(follows_list)

        fans_each_list = re.findall('.*?<a href="/users/(.*?)/" class="name">.*?', data_need[1])  # 获取互粉好友列表
        fan_each_items = FansEachItem()
        fan_each_items["_id"] = re.findall(".*?users/(.*?)/followers/", response.url)[0]
        fan_each_items["fans_each"] = fans_each_list
        id_list.extend(fans_each_list)

        fans_list = re.findall('.*?<a href="/users/(.*?)/" class="name">.*?', data_need[2])  # 获取粉丝列表
        fan_items = FansItem()
        fan_items["_id"] = re.findall(".*?users/(.*?)/followers/", response.url)[0]
        fan_items["fans"] = fans_list
        id_list.extend(fans_list)

        yield follow_items
        yield fan_each_items
        yield fan_items

        for user_id in id_list:
            yield Request(url="http://www.qiushibaike.com/users/{0}/".format(user_id), callback=self.parse_information)
            yield Request(url="http://www.qiushibaike.com/users/{0}/followers/".format(user_id),
                          callback=self.parse_follows_fans)
