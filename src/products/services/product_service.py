from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum, Prefetch
from django.shortcuts import get_object_or_404

from src.games.models import TabItem
from src.products.models import Product, SubFilter, Filter
from src.products.schemas import ProductCountPriceIn
from src.products.utils import paginate


class ProductService:

    @staticmethod
    def get_product_by_id(product_id):
        pr_filters = Prefetch('filters', queryset=Filter.objects.all(), )
        product = Product.objects.prefetch_related(pr_filters).get(id=product_id)
        return product

    @staticmethod
    def count_product_price(count_schema: ProductCountPriceIn):
        product = get_object_or_404(Product, id=count_schema.product_id)
        total_price = product.price
        if count_schema.attributes:
            total_price = total_price + \
                          SubFilter.objects.filter(id__in=count_schema.attributes).aggregate(extra_price=Sum('price'))[
                              'extra_price']
        if product.sale_active():
            sale = (total_price * product.sale_percent) / 100
            total_price = total_price - sale
        return total_price

    @staticmethod
    def hot_products_filter(page: int, page_size: int, game_id=None):
        if game_id:
            items = Product.objects.hot_all(game_id=game_id)
        else:
            items = Product.objects.hot_all()
        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def best_sellers(page: int, page_size: int):
        items = Product.objects.bestsellers()
        return paginate(items=items, page=page, page_size=page_size)

    @staticmethod
    def hot_products_main():
        products = Product.objects.hot_all()
        count = products.count() / 4
        if count % 4 != 0:
            count = int(count) + 1
        return {
            'items': products[:4],
            'count': count
        }

    @staticmethod
    def get_products_by_catalog(catalog_id: int):
        products = Product.objects.filter(catalog_page=catalog_id)
        return products

    @staticmethod
    def get_tab_content(tab_id: int):
        tab = get_object_or_404(TabItem, id=tab_id)
        return tab

    @staticmethod
    def get_tabs(product_id: int):
        tabs = TabItem.objects.filter(tab__product=product_id)
        return tabs
