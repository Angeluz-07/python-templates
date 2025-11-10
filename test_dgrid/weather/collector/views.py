from .models import *
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CollectionRequestSerializer
from weather.settings import OPEN_WEATHER_API_KEY

import json
import asyncio
from  weather.settings import CITY_IDS_FP


@api_view(['GET'])
def collection_request_creation_progress(request, pk):  
    collection_request_id = pk
    current_data = get_cache_current_results(collection_request_id)
    if current_data is None:        
        return Response({'result': 1}, status=status.HTTP_200_OK)        
    total = load_city_ids()
    result = len(current_data)/len(total)
    return Response({'result': result}, status=status.HTTP_200_OK)


def load_city_ids():
    with open(CITY_IDS_FP) as f:
        result = json.load(f)['ids']
    return result

def cache_current_results(collection_request_id, new_data):
    from django.core.cache import cache
    current_data = cache.get(collection_request_id, [])
    cache.set(collection_request_id, current_data + [new_data], timeout=300)
    return None

def get_cache_current_results(collection_request_id):
    from django.core.cache import cache
    current_data = cache.get(collection_request_id)
    return current_data

def reset_cache(collection_request_id):
    from django.core.cache import cache
    cache.delete(collection_request_id)
    return None

async def create_weather_info_item(city_id, collection_request_id, session):
    url = f'http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={OPEN_WEATHER_API_KEY}&units=metric'
    resp = await session.request(method="POST", url=url)
    result = await resp.json()
    cache_current_results(
        collection_request_id,
        {
            'city_id' :city_id,
            'temperature' : result['main']['temp'],
            'humidity' : result['main']['humidity']
        }
    )
    return None

async def schedule_n_seconds(n):
    await asyncio.sleep(n)

async def gather_weather_info(collection_request_id):
    city_ids = load_city_ids() 
    from aiohttp import ClientSession
    for i in range(0, len(city_ids), 60):
        slice = city_ids[i:i+60]         
        tasks = []
        session = ClientSession()
        for city_id in slice: 
            tasks.append(
                create_weather_info_item(city_id, collection_request_id, session)
            )

        last_iteration = (i == list(range(0, len(city_ids), 60))[-1])
        if not last_iteration:
            tasks.append(schedule_n_seconds(60))

        await asyncio.gather(*tasks)
        await session.close()


@api_view(['GET'])
def get_collection_request(request, pk):
    cr = get_object_or_404(CollectionRequest.objects, id=pk)
    serializer = CollectionRequestSerializer(cr)
    return Response(serializer.data)

@api_view(['GET','POST','DELETE'])
def collection_request(request):
    if request.method == 'GET':
        items = CollectionRequest.objects.all()
        serializer = CollectionRequestSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            collection_request_id = serializer.data['id']
            asyncio.run(gather_weather_info(collection_request_id))

            data = get_cache_current_results(collection_request_id)
            cr = get_object_or_404(CollectionRequest.objects, id = collection_request_id)
            cr.city_weather_info=data
            cr.save()
            reset_cache(collection_request_id)
            return Response({'value':'OK'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)