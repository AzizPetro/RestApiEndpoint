import redis

from CacheInterface import ICache


class Cache(ICache):
    def __init__(self):
        self.cache = redis.StrictRedis(host='redis', port=6379, db=0, charset="utf-8", decode_responses=True)
        self.score_table = "score_table"

    def get_rank(self, data):
        return self.cache.zrevrank(self.score_table, data) + 1

    def get_rank_leaderboard(self):
        return self.cache.zrevrange(self.score_table, 0, 9)

    def get_rank_leaderboard_by_country(self, country):
        return self.cache.zrevrange(country, 0, 9)

    def set(self, data):
        self.cache.zadd(self.score_table, {data[0]: data[2]})
        self.cache.zadd(data[1], {data[0]: data[2]})
        return self.cache.zrevrank(self.score_table, data[0]) + 1

    def clear_cache(self):
        self.cache.flushall()

    def init_cache(self,data):
        self.cache.zadd(self.score_table, {data[0]: data[2]})
        self.cache.zadd(data[1], {data[0]: data[2]})