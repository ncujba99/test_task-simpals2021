Test project for fetching data from 999 api
docker-compose up --build 
send a request on 127.0.0.1:8082/find_adverts GET or POST
JSON body provides args for filtering results and pagination.
{
    "pagination":{"from":0, "size":1 },
    "search_query":"test"              
}
Note :
mongo container is exposed on port  27017
elasticsearch is exposed on port 9200 and 9300 (required for kibana)
to disable db ports expose reduce  "27017:27017" to "27017" 
