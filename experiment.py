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
from datetime import timedelta

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
# headers = {
#     "Accept-Language": "uk",
#     # 'Cookie': 'sessionid=oztrs4ue7rmd2mdfihilc8o28jjj9lc0'
# }
# #
# client = httpx.Client()
# #
# # # print(client.post('http://127.0.0.1:8000/api/products/1/to-cart/', headers=headers, json={
# # #     'quantity': 1,
# # #     'attributes': []
# # # }).json())
# # print(client.get(url='http://146.190.122.214/api/orders/my-cart/', headers=headers).content)
# # print(client.get(url='http://146.190.122.214/api/orders/my-cart/', headers=headers).content)
# # print(client.get(url='http://146.190.122.214/api/orders/my-cart/', headers=headers).content)
# # print(client.get(url='http://146.190.122.214/api/orders/my-cart/', headers=headers).content)
# # print(client.get(url="https://goodboost-spacelab.avada-media-dev2.od.ua/api/orders/my-cart/", headers=headers).cookies)
# # print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)
# print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)
# print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)
# print(client.get(url='http://127.0.0.1:8000/api/orders/my-cart/', headers=headers).content)
import pendulum


# import arrow
# now_in_kiev = pendulum.now('Europe/Kiev')
# print(now_in_kiev)
# now = arrow.now()
# last_week_now = now - timedelta(days=7)
# print(last_week_now)
# start_of_week = now.floor('week')
# end_of_week = now.ceil('week')
# print(now)
# print(start_of_week)
# print(end_of_week)








# class Product(models.Model):
#     title = models.CharField(max_length=255)
#     subtitle = models.CharField(max_length=255)
#
#
# class Filter(models.Model):
#     title = models.CharField(max_length=255)
#     product = models.ForeignKey("Product",
#                                 on_delete=models.CASCADE,
#                                 null=True,
#                                 blank=True,
#                                 related_name="filters")
#
#
# class SubFilter(models.Model):
#     title = models.CharField(max_length=255)
#     filter = models.ForeignKey("Filter",
#                                on_delete=models.CASCADE,
#                                related_name="subfilters",
#                                null=True)


