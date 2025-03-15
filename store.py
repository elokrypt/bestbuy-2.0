#  -*- coding: utf-8 -*-
#  @filename store.py
#  @author Marcel Bobolz
#  @last_modified 2025-03-14T22:00:01.128Z
"""
Implements the Store class.
"""

from typing import Optional, List, Tuple
from products import Product

ProductOrder = Tuple[Product, int]


class Store:
    """
    A Store that will hold all of these `Product`s instances,
    and will allow the user to make a purchase of multiple products at once.
    """

    def __init__(self, products: Optional[List[Product]]):
        for product in products:
            if not isinstance(product, Product):
                raise ValueError("Can only add 'Product'(s) to the store.")
        self._products = products

    def add_product(self, product: Product):
        """
        Adds a Product to the store.
        """
        if not isinstance(product, Product):
            raise ValueError("Can only add a Product to the store.")
        self._products.append(product)

    def remove_product(self, product: Product):
        """
        Removes a Product from the store.
        """
        if not isinstance(product, Product):
            raise ValueError("Can only remove a Product from the store.")
        index = 0
        for _product in self._products:
            if _product.name == product.name:
                del self._products[index]
            index += 1

    def get_total_quantity(self) -> int:
        """
        Returns how many items are in the store in total.
        """
        total = 0
        for product in self._products:
            total += product.quantity
        return total

    def get_all_products(self) -> List[Product]:
        """
        Returns all products in the store that are active.
        """
        products_: List[Product] = []
        for product in self._products:
            if product.is_active():
                products_.append(product)
        return products_

    def order(self, shopping_list: List[ProductOrder]) -> float:
        """
        Buys the products and returns the total price of the order.(float)
        """
        total_price: float = 0.00
        for product_order in shopping_list:
            total_price += product_order[0].buy(product_order[-1])
        return total_price


if __name__ == "__main__":
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
    ]

    best_buy = Store(product_list)
    _products = best_buy.get_all_products()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(_products[0], 1), (_products[1], 2)]))
    best_buy.remove_product(_products[2])
