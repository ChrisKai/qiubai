# -*- coding: utf-8 -*-

import sys
import pymongo


class MongoTool(object):
    def __init__(self):
        self.MONGO_HOST = '127.0.0.1'
        self.MONGO_PORT = 27017

    def get_mongo_conn(self):
        try:
            conn = pymongo.MongoClient(self.MONGO_HOST, self.MONGO_PORT)
        except Exception as e:
            print str(e)
            sys.exit()
        return conn

    @staticmethod
    def remove_mongo_collection(conn):
        db = conn['qiubai']
        for item in ['embarrassing_index', 'fans', 'fans_each', 'follows', 'personal_information']:
            print item
            db[item].drop()


if __name__ == '__main__':
    mongo_tool = MongoTool()
    mongo_conn = mongo_tool.get_mongo_conn()
    mongo_tool.remove_mongo_collection(mongo_conn)
