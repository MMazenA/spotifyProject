from flask import Flask
import sqlFunc
import pythonSQLite
from flask_restful import Api, Resource, reqparse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
api = Api(app)
limiter = Limiter(app, key_func=get_remote_address)


song_post_args = reqparse.RequestParser()
song_post_args.add_argument("song_id", type=str, help="Song data")
song_post_args.add_argument("song_name", type=str, help="Song data")
song_post_args.add_argument("artisits", type=str, help="Song data")
song_post_args.add_argument("primary_artist", type=str, help="Song data")
song_post_args.add_argument("song_length", type=str, help="Song data")
song_post_args.add_argument("total_play_count", type=int, help="Song data")
song_post_args.add_argument("current_play_time", type=str, help="Song data")
song_post_args.add_argument("pic_link", type=str, help="Song data")
song_post_args.add_argument("row_id", type=int, help="Row ID")


# ('6Xw3iWrQKgArwlRhVuU9CK', '2SEATER (feat. Aaron Shaw, Samantha Nelson & Austin Feinstein)', 'Tyler, The Creator, Aaron Shaw, Samantha Nelson, Austin Feinstein', 'Tyler, The Creator', '409779', 1, '405694', 'https://i.scdn.co/image/ab67616d0000b273e4bf0d3d9e0224a30ca5f665')


class sptfy_server(Resource):
    decorators = [limiter.limit("60/minute")]

    def get(self):
        return sqlFunc.last_row()

    def post(self):
        args = song_post_args.parse_args()

        sqlFunc.data_insert(args)
        return {"Status": "Sucess"}


class sptfy_local(Resource):
    decorators = [limiter.limit("60/minute")]

    def get(self):
        return pythonSQLite.last_row()

    def post(self):
        args = song_post_args.parse_args()

        pythonSQLite.data_insert(args)
        return {"Status": "Sucess"}


api.add_resource(sptfy_server, "/sptfy_server/")
api.add_resource(sptfy_local, "/sptfy_local/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
