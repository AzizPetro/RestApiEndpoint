import uuid
from datetime import datetime

from flask import jsonify, request
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from cache import Cache
from db_interface import IDb


class Db(IDb):

    def __init__(self):
        self.db_connect = create_engine('sqlite:///user_data.db', echo=True)
        meta = MetaData()
        Table(
            'user_data', meta,
            Column('user_id', String, primary_key=True, default=lambda: str(uuid.uuid4())),
            Column('display_name', String),
            Column('points', Integer),
            Column('country', String),
            Column('timestamp', Integer)
        )
        meta.create_all(self.db_connect)
        self.user_count = 0
        self.cache = Cache()
        self.init_cache()

    def init_cache(self):
        self.cache.clear_cache()
        conn = self.db_connect.connect()
        query = conn.execute("select * from user_data")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        length = len(result)
        if length != 0:
            for element in result:
                data = (element['user_id'], element['country'], element['points'])
                self.cache.set(data)
            self.user_count = len(result)

    def get(self, id):
        conn = self.db_connect.connect()
        query = conn.execute("select * from user_data where user_id ='{0}' ".format(str(id)))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        rank = self.cache.get_rank(id)
        response = {"user_id": id,
                    "display_name": result[0]['display_name'],
                    "points": result[0]['points'],
                    "rank": rank
                    }
        return jsonify(response)

    def get_leaderboard(self):
        conn = self.db_connect.connect()
        rank_list = self.cache.get_rank_leaderboard()
        query = conn.execute("select * from user_data where user_id in {0}".format(tuple(rank_list)))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        for id in rank_list:
            i = 0
            while i < len(result):
                if id == result[i]["user_id"]:
                    result[i]["rank"] = rank_list.index(id) + 1
                    break
                i += 1
        result.sort(key=lambda x: x["rank"])
        return jsonify(result)

    def get_leaderboard_by_country(self, country):
        conn = self.db_connect.connect()
        rank_list = self.cache.get_rank_leaderboard_by_country(country)
        query = conn.execute("select * from user_data where user_id in {0}".format(tuple(rank_list)))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        for id in rank_list:
            i = 0
            while i < len(result):
                if id == result[i]["user_id"]:
                    result[i]["rank"] = rank_list.index(id) + 1
                    break
                i += 1
        result.sort(key=lambda x: x["rank"])
        return jsonify(result)

    def submit_new_user(self):
        conn = self.db_connect.connect()
        print(request.json)
        user_id = str(uuid.uuid4())
        display_name = "gjg_%d" % self.user_count
        score = 0
        try:
            conn.execute("insert into user_data values('{0}','{1}','{2}','{3}','{4}')\
                             ".format(user_id, display_name, score, request.json['country'],
                                      datetime.now().microsecond))
            rank = self.cache.set([user_id, request.json['country'], score])
        except:
            return jsonify({"Couldn't write to database"})

        response = {"user_id": user_id,
                    "display_name": display_name,
                    "points": 0,
                    "rank": rank
                    }
        self.user_count += 1
        return jsonify(response)

    def submit_score(self):
        conn = self.db_connect.connect()
        print(request.json)
        user_id = request.json['user_id']
        score = request.json['score_worth']
        try:
            conn.execute("update user_data set points = {0} where user_id ='{1}'".format(score,
                                                                                         str(user_id)))
        except:
            return jsonify({"Couldn't write to database"})
        query = conn.execute("select * from user_data where user_id ='{0}' ".format(str(user_id)))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        country = result[0]['country']
        self.cache.set([user_id, country, score])
        response = {"user_id": user_id,
                    "points": score,
                    "timestamp": datetime.now().microsecond
                    }
        return jsonify(response)
