from sanic import Sanic
# import redis
import motor.motor_asyncio
import const
import json


class background_service():
    def __init__(self):
        app = Sanic("api 111")

        @app.listener('before_server_start')
        async def setup_db(app, loop):
            self.mongo = motor.motor_asyncio.AsyncIOMotorClient(const.mongo).adminka
            self.redis = redis.StrictRedis(host=const.redis, port=6379, db=0)

        app.run(host='0.0.0.0', port=8082, debug=False, workers=10)

    def get_session_info(self, session):
        # return True
        res = self.redis_con.get(session)
        if res is not None:
            try:
                res = res.decode().replace("'", '"')
                res = json.loads(res)
                return res
            except Exception as eee:
                print(eee)
                return {"type": "error"}
        else:
            return {"type": "unkown"}

    async def find_adverts(self):
        pass
        return
