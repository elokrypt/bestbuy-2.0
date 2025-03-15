#  -*- coding: utf-8 -*-
#  @filename products.py
#  @author Marcel Bobolz
#  @last_modified 2025-03-15T04:35:04.308Z
"""
Implementation of OutOfStockError and Product-class.
"""


class OutOfStockError(Exception):
    """
    Exception raised for Out-Of-Stock scenarios
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Product:
    """
    The Product class represents a specific type of product available in the store
    (For example, MacBook Air M2). It encapsulates information about the product,
    including its name and price.
    Additionally, the Product class includes an attribute to keep track of the
    total quantity of items of that product currently available in the store.
    When someone will purchase it, the amount will be modified accordingly.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a Product.
        """
        if len(name) == 0:
            raise ValueError("argument 'name' cannot be an empty string.")
        self._name = name
        if int(price) < 0:
            raise ValueError("argument 'price' cannot be negative.")
        self._price = price
        if quantity < 0:
            raise ValueError("argument 'quantity' cannot be negative.")
        self._quantity = quantity
        if self._quantity < 1:
            self._active = False
        else:
            self._active = True

    @property
    def name(self) -> str:
        """
        Getter for product-name.
        """
        return self._name

    def get_quantity(self) -> int:
        """
        Getter for quantity.
        """
        return self._quantity

    def set_quantity(self, quantity: int):
        """
        Setter for quantity.
        """
        if quantity < 0:
            raise ValueError("argument 'quantity' cannot be negative.")
        if quantity < 1:
            self.deactivate()
        self._quantity = quantity

    quantity = property(get_quantity, set_quantity)

    def is_active(self) -> bool:
        """
        Getter for active.
        """
        return self._active

    active = property(is_active)

    def activate(self):
        """
        Activates the product.
        """
        self._active = True

    def deactivate(self):
        """
        Deactivates the product.
        """
        self._active = False

    def show(self) -> str:
        """
        Returns a string that represents the product.
        """
        return f"{self._name}, Price: ${self._price}, Quantity: {self._quantity}"

    def buy(self, quantity: int) -> float:
        """
        Updates the quantity of the product.
        Buys a given quantity of the product.
        Returns the total price (float) of the purchase.
        """
        if (self._quantity - quantity) < 0:
            raise OutOfStockError(f"Store cannot provide '{quantity}x {self._name}'.")
        self.quantity -= quantity
        return float(quantity) * self._price


# - eof -
