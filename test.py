import random

def make_sale(price: float, sale: int):
    sale = (price * sale) / 100
    return price - sale
print(make_sale(100,0))