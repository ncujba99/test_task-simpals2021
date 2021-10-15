from elasticsearch.client import Elasticsearch
import const
import os

elastic_con = Elasticsearch(host=const.elastic,
                            port=9200)

index_body = {
    "settings": {
        "analysis": {
            "analyzer": {

            },
            "tokenizer": {

            },
            "char_filter": {

            }
        }
    },
    "mappings": {
        "dynamic": True,
        "properties": {

            "features_groups.features.value":{"type":"text"}

        }
    }
}

elastic_con.indices.create(index='adverts', body=index_body)
