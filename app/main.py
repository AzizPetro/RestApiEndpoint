from flask import Flask
from flask_restful import Api

from database import Db

app = Flask(__name__)
api = Api(app)
database = Db()


@app.route("/")
def home():
    return database.get_leaderboard()


@app.route("/leaderboard", methods=['GET'])
def leaderboard():
    return database.get_leaderboard()


@app.route("/leaderboard/<string:country>", methods=['GET'])
def leaderboard_by_country(country):
    return database.get_leaderboard_by_country(country)


@app.route("/user/profile/<string:user_guid>", methods=['GET'])
def get_user(user_guid):
    return database.get(user_guid)


@app.route("/user/create/", methods=['POST'])
def create_user():
    return database.submit_new_user()


@app.route("/score/submit/", methods=['POST'])
def score_submission():
    return database.submit_score()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
