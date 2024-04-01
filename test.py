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
fake_name = fake.word().capitalize()
fake_email = fake.email()
fake_address = fake.address()

# Print the generated data
print(f"Name: {fake_name}")
print(f"Email: {fake_email}")
print(f"Address: {fake_address}")

var = {
    "instagram_nickname": "@gold_bost",
    "instagram_link": "https://www.youtube.com/",
    "facebook_link": "https://www.youtube.com/",
    "reddit_link": "https://www.youtube.com/",
    "email": "user@example.com",
    "discord_link": "https://www.youtube.com/",
    "whats_up_link": "https://www.youtube.com/",
    "footer_bottom_text": "© 2020. All rights reserved",
    "privacy_policy_link": "https://www.youtube.com/",
    "terms_of_use_link": "https://www.youtube.com/",
    "refund_policy_link": "https://www.youtube.com/",
    "subscribe_sale": 10,
    "address1_en": "Ukraine, Odessa, st. Kosmonavtov, 32",
    "address1_ua": "Українa, м. Одеса, вул. Космонавтів, 32",
    "address2_en": "Ukraine, Odessa, st. Kosmonavtov, 32",
    "address2_ua": "Українa, м. Одеса, вул. Космонавтів, 32",
    "footer_description_en": "We cooperate only with qualified and experienced top world players who participate "
    "personally in each event and ready to provide you with the best boosting service and "
    "gaming experience in your favorite online games. We ensure that every customer is "
    "highly satisfied and 100% positive feedback of our work pretty much sums it up ;) Get "
    "the most relevant eu boost and power leveling.",
    "footer_description_ua": "Ми співпрацюємо лише з кваліфікованими та досвідченими провідними світовими гравцями, "
    "які особисто беруть участь у кожній події та готові надати вам найкращі послуги "
    "підвищення та ігровий досвід у ваших улюблених онлайн-іграх. Ми гарантуємо, "
    "що кожен клієнт буде дуже задоволений, і 100% позитивний відгук про нашу роботу майже "
    "підсумовує це ;) Отримайте найрелевантнішу підтримку та підвищення потужності для ЄС.",
    "header_top_text_en": "leave a trustpilot review and get an extra 10% off your next order!",
    "header_top_text_ua": "залиште відгук Trustpilot і отримайте додаткову знижку 10% на наступне замовлення!",
    "subscribe_form_text_en": "Sing up to our email newsteller and get 10% DISCOUNT on your first order!",
    "subscribe_form_text_ua": "Підпишіться на нашу електронну розсилку та отримайте ЗНИЖКУ 10% на перше замовлення!",
    "address1_link": "https://www.youtube.com/",
    "address2_link": "https://www.youtube.com/",
}
random_image = random.choice(os.listdir(os.path.join("seed", "banner")))

image = open(os.path.join("seed", "banner", random_image), "rb")
print(image.name)
