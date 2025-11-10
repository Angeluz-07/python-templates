## Run app docker-compose (Linux)
1. Install Docker and Docker Compose.
2. Create `.env` from `.env.example`.
3. Set env variables :
```bash
source .env
```
4. Run tests:
```bash
sudo docker-compose build
sudo docker-compose run web_app sh -c "cd weather/; pytest"
```
Tests taks ~4 min to run.


## Services

Start running the service
```bash
sudo docker-compose up
```

Use a http client and make http requests to the following services

### Collect data
POST `http://localhost:8000/collection-request/` 

BODY : 
```
{
    "id" : 1
}
```
example response(takes ~3min to complete) :
```
{
    "value": "OK"
}
```

### Check progress
GET `http://localhost:8000/collection-request/{id}/progress` 

example response :
```
{
    "result": 0.3592814371257485
}
```

### Inpect fully collected data
GET `http://localhost:8000/collection-request/{id}` 

example response :
```
{
    "id":1,
    "created_at":"2021-06-27T01:55:00.255890Z",
    "city_weather_info":[
        {
            "city_id":3440781,
            "humidity":91,
            "temperature":9.87
        },
        {
            "city_id":3441243,
            "humidity":83,
            "temperature":7.56
        },
        ...
    ]
}
```

### Stack
For this exercise Django + Django REST Framework were selected as the tool to develop the service. Django was selected to set up a quick and robust api, abstracting the DB interacion/migrations/data validations logic needed.

For async calls `asyncio` module of python was used. The calls were scheduled to respect the limits of 60 calls per minute in the open-weather api. Also the module `aiohttp` was used to be consistent with async functions implemented and the type of http requests needed.

PostgreSQL was selected to handle the data storage of json data by keeping a relational model as the main data model. The integration of services was set up with docker-compose and docker.

The development was Test-driven using pytest-django and pytest-asyncio to fully test the async functions developed. There was a challenge given that Django ORM doesnt work smoothly with async functions. So, it was needed to use Django cache to keep track of the progress of the data collected. For a more scalable solution it would be needed to use another service(maybe redis or an in-memory DB), but for this exercise django cache worked fine.
