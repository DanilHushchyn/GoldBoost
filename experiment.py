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

payload = {
    "first_name": "string",
    "last_name": "string",
    "payment_method": "PayPal",
    "communication": "Telegram",
    "notify_me": True
}
for i in range(1, 4):
    a ={
        'pk': int(f'{i}0{i}'),
        'title_en': '...',
        'title_uk': '...',
        'order': i,
        'price': i * 10,
    }
    print(a)
