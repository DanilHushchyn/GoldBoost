import json
import random

import pytest
import os
from pathlib import Path

from django.utils import timezone

from config import settings
import environ
import pytest
from datetime import timedelta

from ninja_extra.testing import TestClient
from ninja_jwt.schema_control import SchemaControl
from loguru import logger
from src.games.models import CatalogPage
from src.main.utils import make_request
from src.products.api import ProductController
from src.products.models import Product, Filter, SubFilter
from src.users.api import CustomTokenObtainPairController
from ninja_jwt.settings import api_settings
from django.core.files import File

from faker import Faker

import httpx

from src.users.schemas import MessageOutSchema

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# django-environ
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

import pytest
from django.db import connections

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def run_sql(sql):
    conn = psycopg2.connect(database='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings

    the_source_db = settings.DATABASES['default']['NAME']
    logger.debug()
    # run_sql('DROP DATABASE IF EXISTS the_copied_db')
    run_sql(f'CREATE DATABASE test_{the_source_db} TEMPLATE {the_source_db}')

    yield

    for connection in connections.all():
        connection.close()

    run_sql(f'DROP DATABASE test_{the_source_db}')


@pytest.fixture(scope='session')
def django_db_setup():
    logger.debug(settings.DATABASES['default']['NAME'])
    settings.DATABASES['default'] = {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME_TEST"),
        "USER": env("DB_USER"),
        # "TEST": {
        #     "NAME": env("DB_NAME_TEST"),
        #
        # },
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }


obtain_token_client = TestClient(CustomTokenObtainPairController)
headers = {
    'Accept-Language': 'en'
}

schema = SchemaControl(api_settings)
obtain_pair_schema = schema.obtain_pair_schema.get_response_schema()


@pytest.fixture(scope="session")
def access_token():
    auth = {
        "password": "sword123",
        "email": "user@example.com",
    }
    response = httpx.post('http://127.0.0.1:8000/api/token/pair',
                          headers=headers, json=auth)
    assert response.status_code == 200
    token = response.json()['access']
    return f'Bearer {token}'


@pytest.fixture
def product_with_range():
    catalog_ids = CatalogPage.objects.values_list('id', flat=True)
    random_card_image = random.choice(os.listdir(os.path.join("seed", "card_image")))
    random_image = random.choice(os.listdir(os.path.join("seed", "banner")))
    card_image = open(os.path.join("seed", "card_image", random_card_image), "rb")
    image = open(os.path.join("seed", "banner", random_image), "rb")
    current_datetime = timezone.now()

    product = Product.objects.create(
        **{
            "title_en": '...',
            "title_uk": '...',
            "subtitle_en": '...',
            "subtitle_uk": '...',
            "image": File(image, "/media/" + image.name),
            "card_img": File(card_image, "/media/" + card_image.name),
            "card_img_alt_en": '...',
            "card_img_alt_uk": '...',
            "image_alt_en": '...',
            "image_alt_uk": '...',
            "description_en": "...",
            "description_uk": "...",
            "price": 100,
            "price_type": "range",
            "bonus_points": 100,
            "sale_percent": 10,
            "sale_from": current_datetime - timedelta(days=1),
            "sale_until": current_datetime + timedelta(days=1),
            "bought_count": 0,
            "catalog_page_id": random.choice(catalog_ids),
        }
    )
    filters = [
        {
            'title_en': '...',
            'title_uk': '...',
            'type': 'Select',
            'product': product,
            'order': 1,

        },
        {
            'title_en': '...',
            'title_uk': '...',
            'type': 'Radio',
            'product': product,
            'order': 2,

        },
        {
            'title_en': '...',
            'title_uk': '...',
            'type': 'Checkbox',
            'product': product,
            'order': 3,

        },
        {
            'title_en': '...',
            'title_uk': '...',
            'type': 'Slider',
            'product': product,
            'order': 4,

        },
    ]
    for i, data in enumerate(filters):
        fltr = Filter.objects.create(**data)
        for j in range(1, 5):
            SubFilter(**{
                'id': f'{i}00{j}',
                'title_en': '...',
                'title_uk': '...',
                'order': j,
                'filter': fltr,
                'price': j * 10,
            })
    return product


@pytest.fixture
def products_to_cart(access_token) -> int:
    product = Product.objects.filter(price_type='fixed').first()
    client = TestClient(ProductController)
    request_str = f'/{product.id}/to-cart/'
    payload = {
        'attributes': [],
        'quantity': 1,
    }
    headers['Authorization'] = access_token
    count = 4
    for i in range(count):
        response, is_valid = make_request(request_str=request_str,
                                          schema=MessageOutSchema,
                                          client=client,
                                          method='post',
                                          payload=json.dumps(payload),
                                          headers=headers)
        assert is_valid is True
        assert response.status_code == 200

    return count
