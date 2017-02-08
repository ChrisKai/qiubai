# -*- coding:utf-8 -*-

import sys
import redis


class RedisTool(object):
    def __init__(self):
        self.REDIS_HOST = '127.0.0.1'
        self.REDIS_PORT = 6379

    def get_redis_conn(self):
        try:
            conn = redis.Redis(self.REDIS_HOST, self.REDIS_PORT)
        except Exception as e:
            print str(e)
            sys.exit()
        return conn

    @staticmethod
    def remove_redis_key(conn):
        for keys in conn.keys():
            print keys
            conn.delete(keys)

if __name__ == "__main__":
    redis_tool = RedisTool()
    redis_conn = redis_tool.get_redis_conn()
    redis_tool.remove_redis_key(redis_conn)
