# -*- coding: utf-8 -*-
# # Replace 'username' with the username of the profile you want to fetch posts from
# profile = instaloader.Profile.from_username(loader.context, '@thegutstuff')
#
# # Iterate over the posts and print their URLs
# for post in profile.get_posts():
#     print(post.url)
import json
import os
import random

import httpx

# In your Django project, import the Faker library
# from faker import Faker
# from faker.providers import internet, person,date_time
#
# # Create an instance of the Faker class
# fake = Faker("en_US")
# fake.add_provider(internet)
# fake.add_provider(person)
# fake.add_provider(date_time)
# # Generate a fake name, email and address
# fake_name = fake.name()
# fake_email = fake.email()
# fake_address = fake.address()
# words = fake.date()
# words = fake.time()
# # Print the generated data
# print(f"Name: {fake_name}")
# print(f"Words: {words}")
# print(f"Name: {fake.sentence(nb_words=3)}")
# print(f"Email: {fake_email}")
# print(f"Address: {fake_address}")
headers = {
    'Accept-Language': 'uk'
}
# print(httpx.post('http://127.0.0.1:8000/api/products/1/to-cart/', headers=headers, json={
#     'quantity': 1,
#     'attributes': []
# }).json())
client = httpx.Client()

print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)

print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)
print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)
print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)
