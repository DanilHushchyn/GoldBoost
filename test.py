# -*- coding: utf-8 -*-
# # Replace 'username' with the username of the profile you want to fetch posts from
# profile = instaloader.Profile.from_username(loader.context, '@thegutstuff')
#
# # Iterate over the posts and print their URLs
# for post in profile.get_posts():
#     print(post.url)
import os
import random

# In your Django project, import the Faker library
from faker import Faker
from faker.providers import internet, person

# Create an instance of the Faker class
fake = Faker("uk_Ua")
fake.add_provider(internet)
fake.add_provider(person)
# Generate a fake name, email and address
fake_name = fake.name()
fake_email = fake.email()
fake_address = fake.address()

# Print the generated data
print(f"Name: {fake_name}")
print(f"Name: {fake.sentence(nb_words=3)}")
print(f"Email: {fake_email}")
print(f"Address: {fake_address}")


