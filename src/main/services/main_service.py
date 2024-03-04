from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404

from src.main.models import WhyChooseUs, Review, News, Insta, Setting
from src.products.models import Product
from src.products.utils import paginate


class MainService:

    @staticmethod
    def get_why_choose_us():
        objects = WhyChooseUs.objects.all()
        return objects

    @staticmethod
    def get_instagram():
        objects = Insta.objects.all()
        return objects

    @staticmethod
    def get_reviews(page: int, page_size: int):
        items = Review.objects.all()
        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def get_settings():
        return Setting.objects.first()

    @staticmethod
    def get_news(page: int, page_size: int):
        items = News.objects.all()
        return paginate(items=items, page=page, page_size=page_size)

    # def get_main(self):
    #     reviews = self.get_reviews()
    #     news = self.get_news()
    #     insta = Insta.objects.all()
    #     insta_imgs = [obj.img.url for obj in insta]
    #     return {
    #         'why_choose_us': WhyChooseUs.objects.all(),
    #         'reviews': {
    #             'items': reviews[:self._reviews_count],
    #             'count': pages_count(queryset_len=reviews.count(), page_size=self._reviews_count)
    #         },
    #         'news': {
    #             'items': news[:self._news_count],
    #             'count': pages_count(queryset_len=news.count(), page_size=self._news_count)
    #         },
    #         'instagram': insta_imgs,
    #     }
