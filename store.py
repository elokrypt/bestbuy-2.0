#  -*- coding: utf-8 -*-
#  @filename store.py
#  @author Marcel Bobolz
#  @last_modified 2025-03-15T12:38:22.585Z
"""
Implements the Store class.
"""

from typing import Optional, List, Tuple
from products import Product
from products import OutOfStockValueError, MaximumValueError

ProductOrder = Tuple[Product, int]


class Store:
    """
    A Store that will hold all of these `Product`s instances,
    and will allow the user to make a purchase of multiple products at once.
    """

    def __init__(self, products: Optional[List[Product]]):
        for product in products:
            if not isinstance(product, Product):
                raise ValueError(
                    "'product' is not an instance of List[Product]"
                )
        self._products = products

    def __add__(self, other_store) -> object:
        """
        Creates a new instance of Store by accumulating all additional
        products in the second Store instance to the first named store
        instance.
        Raises an exception if there are duplicate products in one
        of the other store instances.
        """
        new_store: Store = Store(self._products)
        for other_product in other_store.products:
            if other_product not in new_store:
                new_store.add_product(other_product)
            else:
                raise ValueError(
                    f"The product '{other_product}' already exists."
                )
        return new_store

    def __contains__(self, product) -> bool:
        """
        Checks if a product is available in the store. (name-check)
        """
        for prod in self._products:
            if prod.name == product.name:
                return True

    @property
    def products(self):
        """
        Returns all products in the store, even the inactive ones.
        """
        return self._products

    def add_product(self, product: Product):
        """
        Adds a Product to the store.
        """
        if not isinstance(product, Product):
            raise ValueError("'product' is not an instance of Product(..)")
        self._products.append(product)

    def remove_product(self, product: Product):
        """
        Removes a Product from the store.
        """
        if not isinstance(product, Product):
            raise ValueError("'product' is not an instance of Product(..)")
        index = 0
        for _product in self._products:
            if _product.name == product.name:
                self._products.pop(index)
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
        products: List[Product] = []
        for product in self._products:
            if product.is_active():
                products.append(product)
        return products

    def order(self, shopping_list: List[ProductOrder]) -> float:
        """
        Buys the product(s) with given quantity, and accumulates
        the total price of the order.
        Returns the total price as float.
        """
        total_price: float = 0.00
        for product_order in shopping_list:
            try:
                total_price += product_order[0].buy(product_order[-1])
            except OutOfStockValueError as e:
                print(f"Error:\n\t{e.message}")
            except MaximumValueError as e:
                print(f"Error:\n\t{e.message}")
        return total_price


# - eof -
