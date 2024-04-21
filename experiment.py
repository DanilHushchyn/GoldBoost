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
from faker import Faker
from faker.providers import date_time, internet, person

#
# Create an instance of the Faker class
# fake = Faker("en_US")
# fake_ua = Faker("uk_UA")
# print(' '.join(fake.name().split()))
# print(fake.name())
# print(fake_ua.name())
# print(str([word.capitalize() for word in fake.name().split()]))
# fake.add_provider(person)
# print(fake.text(max_nb_chars=600))
# print(fake_ua.name())
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
    "Accept-Language": "uk",
    # 'Cookie': 'sessionid=oztrs4ue7rmd2mdfihilc8o28jjj9lc0'
}
#
client = httpx.Client()
#
# # print(client.post('http://127.0.0.1:8000/api/products/1/to-cart/', headers=headers, json={
# #     'quantity': 1,
# #     'attributes': []
# # }).json())
# print(client.get(url='http://146.190.122.214/api/orders/my-cart/', headers=headers).content)
# print(client.get(url='http://146.190.122.214/api/orders/my-cart/', headers=headers).content)
# print(client.get(url='http://146.190.122.214/api/orders/my-cart/', headers=headers).content)
# print(client.get(url='http://146.190.122.214/api/orders/my-cart/', headers=headers).content)
print(client.get(url="http://127.0.0.1:8000/api/orders/my-cart/", headers=headers).cookies)
# print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)
# print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)
