import asyncio
import motor.motor_asyncio
import requests
import json
from elasticsearch import AsyncElasticsearch
import const


def get_adverts(username="", password=""):
    adverts = []
    res_count = 1
    page = 1
    while res_count > 0:
        response = requests.get('https://partners-api.999.md/adverts?page_size=10&page='
                                + str(page) + '&states=blocked,blocked_commercial,need_pay,hidden,expired',
                                auth=(username, password))
        data = json.loads(response.text)
        res_count = len(data["adverts"])
        adverts.extend(data["adverts"])
        page = page + 1

    return adverts


def get_advert_details(username="", password="", id=""):
    response = requests.get('https://partners-api.999.md/adverts/' + id,
                            auth=(username, password))

    if response.status_code != 404:
        return json.loads(response.text)
    else:
        return None


async def sync_adverts():
    mongo_db = motor.motor_asyncio.AsyncIOMotorClient(const.mongo).simpals
    es = AsyncElasticsearch(const.elastic)

    while 1:
        adverts = get_adverts(username=const.api_login, password=const.api_password)
        for advert in adverts:
            advert_details = get_advert_details(username=const.api_login, password=const.api_password, id=advert["id"])
            for key in advert_details:
                advert[key] = advert_details[key]
            await mongo_db.adverts.update_one({"id": advert["id"]}, {"$set": advert}, upsert=True)
            await es.index(index="adverts", id=advert["id"], body=advert)
        await asyncio.sleep(10)


loop = asyncio.get_event_loop()
loop.create_task(sync_adverts())
loop.run_forever()
