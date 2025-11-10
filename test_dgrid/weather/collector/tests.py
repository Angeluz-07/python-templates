from django.test import  AsyncClient

from .models import *
from .views import load_city_ids, gather_weather_info, reset_cache
from rest_framework import status

# Create your tests here.
import pytest
import asyncio


def test_load_city_ids(): 
    l = load_city_ids()
    assert 3439525 in l
    assert 167 == len(l)

@pytest.mark.asyncio
async def test_collection_request_creation_progress(client):
    collection_request_id = 1
    task = asyncio.create_task(gather_weather_info(collection_request_id))

    await asyncio.sleep(60)
    response = client.get('/collection-request/1/progress')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['result'] > 0.3 and  response.json()['result'] < 0.4

    await task
    reset_cache(collection_request_id)
    
    response = client.get('/collection-request/1/progress')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['result'] == 1

@pytest.mark.django_db(transaction=True)
def test_collection_request(client):
    response = client.post('/collection-request/', data={'id':1})
    assert response.status_code == status.HTTP_201_CREATED

    cr =  CollectionRequest.objects.first()
    assert hasattr(cr,'created_at')

    current_ids = list(map(lambda x : x['city_id'] , cr.city_weather_info))
    expected_ids = load_city_ids() 
    assert sorted(current_ids) == sorted(expected_ids)

@pytest.mark.django_db(transaction=True)
def test_get_collection_request(client):
    cr = CollectionRequest(id=1)
    cr.save()

    response = client.get('/collection-request/1')
    assert response.status_code == status.HTTP_200_OK
