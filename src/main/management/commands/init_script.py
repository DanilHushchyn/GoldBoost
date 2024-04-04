# -*- coding: utf-8 -*-
import os
import random

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from psycopg2.sql import NULL

from src.games.models import *
from src.main.models import *
from src.products.models import *

User = get_user_model()
fake = Faker()
fake.word()


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.fake_en = Faker("en_US")
        self.fake_uk = Faker("uk_UA")

    def handle(self, null=None, *args, **options):
        self._create_superuser()
        self._create_games()
        self._create_main_page()
        self._create_pages()
        self._create_products()

    def _create_superuser(self):
        user = User.objects.create(
            first_name=self.fake_en.first_name_male(),
            last_name=self.fake_en.last_name_male(),
            email="user@example.com",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password("sword123")
        user.save()

    def _create_games(self):
        random_filter_logo = random.choice(os.listdir(os.path.join("seed", "filter_logo")))
        random_product_logo = random.choice(os.listdir(os.path.join("seed", "product_logo")))
        filter_logo = open(os.path.join("seed", "filter_logo", random_filter_logo), "rb")
        product_logo = open(os.path.join("seed", "product_logo", random_product_logo), "rb")
        print(filter_logo.name)
        for i in range(3):
            game = Game.objects.create(
                name=self.fake_en.unique.word().capitalize(),
                logo_filter=File(filter_logo, "/media/" + filter_logo.name),
                logo_product=File(product_logo, "/media/" + product_logo.name),
                logo_product_alt_en=self.fake_en.word(),
                logo_product_alt_uk=self.fake_uk.word(),
                logo_filter_alt_en=self.fake_en.word(),
                logo_filter_alt_uk=self.fake_uk.word(),
                order=i,
            )
            game.save()

    def _create_pages(self):
        for game in Game.objects.all():
            for j in range(5):
                page = CatalogPage.objects.create(
                    title_en=self.fake_en.word().capitalize(),
                    title_uk=self.fake_uk.word().capitalize(),
                    description_en=self.fake_en.text(max_nb_chars=500).capitalize(),
                    description_uk=self.fake_uk.text(max_nb_chars=500).capitalize(),
                    parent=None,
                    game_id=game.id,
                    order=j,
                )
                for i in range(4):
                    CatalogTabs.objects.create(
                        title_en=self.fake_en.word().capitalize(),
                        title_uk=self.fake_uk.word().capitalize(),
                        content_en=self.fake_en.text(max_nb_chars=500).capitalize(),
                        content_uk=self.fake_uk.text(max_nb_chars=500).capitalize(),
                        order=i,
                        catalog_id=page.id,
                    )

    def _create_main_page(self):
        obj = {
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
            "address1_uk": "Українa, м. Одеса, вул. Космонавтів, 32",
            "address2_en": "Ukraine, Odessa, st. Kosmonavtov, 32",
            "address2_uk": "Українa, м. Одеса, вул. Космонавтів, 32",
            "footer_description_en": "We cooperate only with qualified and experienced top world players who participate "
            "personally in each event and ready to provide you with the best boosting service and "
            "gaming experience in your favorite online games. We ensure that every customer is "
            "highly satisfied and 100% positive feedback of our work pretty much sums it up ;) Get "
            "the most relevant eu boost and power leveling.",
            "footer_description_uk": "Ми співпрацюємо лише з кваліфікованими та досвідченими провідними світовими гравцями, "
            "які особисто беруть участь у кожній події та готові надати вам найкращі послуги "
            "підвищення та ігровий досвід у ваших улюблених онлайн-іграх. Ми гарантуємо, "
            "що кожен клієнт буде дуже задоволений, і 100% позитивний відгук про нашу роботу майже "
            "підсумовує це ;) Отримайте найрелевантнішу підтримку та підвищення потужності для ЄС.",
            "header_top_text_en": "leave a trustpilot review and get an extra 10% off your next order!",
            "header_top_text_uk": "залиште відгук Trustpilot і отримайте додаткову знижку 10% на наступне замовлення!",
            "subscribe_form_text_en": "Sing up to our email newsteller and get 10% DISCOUNT on your first order!",
            "subscribe_form_text_uk": "Підпишіться на нашу електронну розсилку та отримайте ЗНИЖКУ 10% на перше "
            "замовлення!",
            "address1_link": "https://www.youtube.com/",
            "address2_link": "https://www.youtube.com/",
        }
        Setting.objects.create(**obj)
        for j in range(6):
            random_image = random.choice(os.listdir(os.path.join("seed", "insta_imgs")))
            image = open(os.path.join("seed", "insta_imgs", random_image), "rb")
            Insta.objects.create(
                img=File(image, "/media/" + image.name),
                img_alt_uk=self.fake_uk.word().capitalize(),
                img_alt_en=self.fake_en.word().capitalize(),
            )
        for j in range(20):
            Review.objects.create(
                author_en=self.fake_en.name().capitalize(),
                author_uk=self.fake_uk.name().capitalize(),
                source_of_review="dving.net",
                stars_count=self.fake_en.pyint(min_value=1, max_value=5),
                source_of_review_url="https://meet.google.com/",
                comment_en=self.fake_en.text(max_nb_chars=120).capitalize(),
                comment_uk=self.fake_uk.text(max_nb_chars=120).capitalize(),
            )
        for game in Game.objects.all():
            random_image = random.choice(os.listdir(os.path.join("seed", "news")))
            image = open(os.path.join("seed", "news", random_image), "rb")
            for i in range(6):
                News.objects.create(
                    title_en=self.fake_en.word().capitalize(),
                    title_uk=self.fake_uk.word().capitalize(),
                    description_en=self.fake_en.text(max_nb_chars=150).capitalize(),
                    description_uk=self.fake_uk.text(max_nb_chars=150).capitalize(),
                    image_alt_en=self.fake_en.word(),
                    image_alt_uk=self.fake_uk.word(),
                    game_id=game.id,
                    image=File(image, "/media/" + image.name),
                )
        for j in range(3):
            random_icon = random.choice(os.listdir(os.path.join("seed", "why_choose_us")))
            icon = open(os.path.join("seed", "why_choose_us", random_icon), "rb")
            WhyChooseUs.objects.create(
                title_en=self.fake_en.word().capitalize(),
                title_uk=self.fake_uk.word().capitalize(),
                description_en=self.fake_en.text(max_nb_chars=150).capitalize(),
                description_uk=self.fake_uk.text(max_nb_chars=150).capitalize(),
                icon=File(icon, "/media/" + icon.name),
                icon_alt_en=self.fake_en.word().capitalize(),
                icon_alt_uk=self.fake_uk.word().capitalize(),
            )

    def _create_products(self):
        random_card_image = random.choice(os.listdir(os.path.join("seed", "card_image")))
        random_image = random.choice(os.listdir(os.path.join("seed", "banner")))
        card_image = open(os.path.join("seed", "card_image", random_card_image), "rb")
        image = open(os.path.join("seed", "banner", random_image), "rb")
        for page in CatalogPage.objects.all():
            for i in range(3):
                product = Product.objects.create(
                    title_en=self.fake_en.sentence(nb_words=3).capitalize(),
                    title_uk=self.fake_uk.sentence(nb_words=3).capitalize(),
                    subtitle_en=self.fake_en.sentence(nb_words=3).capitalize(),
                    subtitle_uk=self.fake_uk.sentence(nb_words=3).capitalize(),
                    description_en=self.fake_en.text(max_nb_chars=150).capitalize(),
                    description_uk=self.fake_uk.text(max_nb_chars=150).capitalize(),
                    bonus_points=self.fake_en.pyint(min_value=10, max_value=150),
                    catalog_page_id=page.id,
                    price_type="range" if i == 1 else "fixed",
                    price=self.fake_en.pyint(min_value=5, max_value=600),
                    image=File(image, "/media/" + image.name),
                    card_img=File(card_image, "/media/" + card_image.name),
                    card_img_alt_en=self.fake_en.word(),
                    card_img_alt_uk=self.fake_uk.word(),
                    image_alt_en=self.fake_en.word(),
                    image_alt_uk=self.fake_uk.word(),
                )
                product.save()

                for j in range(4):
                    ProductTabs.objects.create(
                        title_en=self.fake_en.word().capitalize(),
                        title_uk=self.fake_uk.word().capitalize(),
                        content_en=self.fake_en.text(max_nb_chars=500).capitalize(),
                        content_uk=self.fake_uk.text(max_nb_chars=500).capitalize(),
                        product_id=product.id,
                        order=j,
                    )
        for prod in Product.objects.filter(price_type='range'):
            for j in range(4):
                filter_obj = Filter.objects.create(
                    title_en=self.fake_en.word().capitalize(),
                    title_uk=self.fake_uk.word().capitalize(),
                    type=random.choice(["Slider", "Radio", "CheckBox", "Select"]),
                    product_id=prod.id,
                    order=j,
                )
                for k in range(4):
                    SubFilter.objects.create(
                        title_en=self.fake_en.word().capitalize(),
                        title_uk=self.fake_uk.word().capitalize(),
                        filter_id=filter_obj.id,
                        price=self.fake_en.pyint(min_value=5, max_value=100),
                        order=k,
                    )
