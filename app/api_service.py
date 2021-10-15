from sanic import Sanic
from sanic import response
from elasticsearch import AsyncElasticsearch
# import redis
import motor.motor_asyncio
import const
import json


class background_service():
    def __init__(self):
        app = Sanic("api 111")

        app.add_route(self.find_adverts, '/find_adverts', methods=['GET', "POST"])

        @app.listener('before_server_start')
        async def setup_db(app, loop):
            # self.mongo = motor.motor_asyncio.AsyncIOMotorClient(const.mongo).adminka
            # self.redis = redis.StrictRedis(host=const.redis, port=6379, db=0)
            self.es = AsyncElasticsearch(const.elastic)

        app.run(host='0.0.0.0', port=8082, debug=False, workers=10)

    # def get_session_info(self, session):
    #     # return True
    #     res = self.redis_con.get(session)
    #     if res is not None:
    #         try:
    #             res = res.decode().replace("'", '"')
    #             res = json.loads(res)
    #             return res
    #         except Exception as eee:
    #             print(eee)
    #             return {"type": "error"}
    #     else:
    #         return {"type": "unkown"}

    async def find_adverts(self, request):

        try:
            args = json.loads(request.body.decode())
            pagination = {"from": int(args["pagination"]["from"]),
                          "size": int(args["pagination"]["size"])}
            search_query = args["search_query"]
        except:
            return response.json({"status": "wrong_args"})

        elastic_request = {"size": pagination["size"],
                           "from": pagination["from"],
                           "query": {"bool": {"must": []}}
                           }
        elastic_request["query"]["bool"]["must"].append(

            {
                "match": {"title": search_query}
            }
        )

        elastic_response = await self.es.search(body=elastic_request, index="adverts")

        results = [x["_source"] for x in elastic_response["hits"]["hits"]]

        return response.json({"results":results})
