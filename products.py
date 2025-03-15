#  -*- coding: utf-8 -*-
#  @filename products.py
#  @author Marcel Bobolz
#  @last_modified 2025-03-15T07:56:17.533Z
"""
Implementation of Product class interface, plus OutOfStockError
and NonStockedProduct + LimitedProduct subclasses
"""

from abc import ABC, abstractmethod


class MaximumValueError(Exception):
    """
    Exception raised for maximum-value per order edge-cases.
    """

    def __init__(self, name, maximum):
        self.message = f"Reason: store provides only {maximum}x '{name}' per order"
        super().__init__(self.message)


class OutOfStockValueError(Exception):
    """
    Exception raised for Out-Of-Stock scenarios
    """

    def __init__(self, name, quantity):
        self.message = f"Reason: store cannot provide {quantity}x '{name}'"
        super().__init__(self.message)


class BaseProduct(ABC):
    @property
    def name(self) -> str:
        """
        Getter for product-name.
        """
        return self._name

    @property
    def quantity(self) -> int:
        """
        Getter for quantity.
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        """
        Setter for quantity.
        """
        if quantity < 0:
            raise ValueError("argument 'quantity' cannot be negative.")
        if quantity < 1:
            self.deactivate()
        self._quantity = quantity

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

    @abstractmethod
    def show(self) -> str:
        """
        Returns a string that represents the product.
        """
        pass

    @abstractmethod
    def buy(self, quantity: int) -> float:
        """
        Checks the quantity, if inside available boundaries.
        Returns the total price (float) of the purchase.
        """
        pass


class Product(BaseProduct):
    """
    The Product class represents a specific type of product available in the
    store (For example, MacBook Air M2).
    It encapsulates information about the product,including its name and price.
    Additionally, the Product class includes an attribute to keep track of the
    total quantity of items of that product currently available in the store.
    When someone will purchase it, the amount will be modified accordingly.
    """

    def __init__(self, name: str, price: float | int, quantity: int):
        """
        Initializes a Product.
        """
        self.activate()
        if len(name) == 0:
            raise ValueError("argument 'name' cannot be an empty string.")
        self._name = name
        if float(price) < 0.00:
            raise ValueError("argument 'price' cannot be negative.")
        self._price = float(price)
        if int(quantity) < 0:
            raise ValueError("argument 'quantity' cannot be negative.")
        self.quantity = int(quantity)

    def show(self) -> str:
        """
        Returns a string that represents the product.
        """
        return (
            f"'{self._name}', Price: ${self._price:.2f}, "  # @format
            f"Quantity: {self.quantity}"
        )

    def buy(self, quantity: int) -> float:
        """
        Checks the quantity, if inside available boundaries.
        Updates the quantity of the product.
        Returns the total price (float) of the purchase.
        """
        if int(quantity) <= 0:
            raise ValueError("argument 'quantity' must be >= 1 to buy a product")
        if (self._quantity - int(quantity)) < 0:
            raise OutOfStockValueError(self._name, quantity)
        self.quantity -= int(quantity)
        return float(quantity) * self._price


class NonStockedProduct(Product):
    """
    Some products in the store are not physical,
    so we dont need to keep track of their quantity.
    for example - a Microsoft Windows license.
    """

    def __init__(self, name: str, price: float | int):
        """
        Initializes a NonStockedProduct.
        """
        super().__init__(name=name, price=price, quantity=0)
        self._quantity = 0

    @property
    def quantity(self) -> int:
        """
        Getter for quantity (=0 -> see class description)
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        """
        Setter for quantity (= 0 -> see class description).
        """
        pass

    def show(self) -> str:
        """
        Returns a string that represents the product.
        """
        return f"'{self._name}', Price: ${self._price:.2f}, Quantity: [infinite]"

    def buy(self, quantity: int) -> float:
        """
        Buys a given quantity of the product.
        """
        if int(quantity) <= 0:
            raise ValueError("argument 'quantity' must be >= 1 to buy a product")
        return float(quantity) * self._price


class LimitedProduct(Product):
    """
    Some products can only be purchased X times in an order.
    For example - a shipping fee can only be added once.
    If an order is attempted with quantity larger than the 'maximum' one,
    it should be refused with an 'OrderLimitedError' exception.
    """

    def __init__(self, name: str, price: float | int, quantity: int, maximum: int):
        """
        Initializes a NonStockedProduct.
        """
        super().__init__(name=name, price=price, quantity=quantity)
        if int(maximum) < 1:
            raise ValueError("argument 'maximum' must be >= 1.")
        self._maximum = int(maximum)

    @property
    def maximum(self) -> int:
        """
        Getter for maximum
        """
        return self._maximum

    def show(self) -> str:
        """
        Returns a string that represents the product.
        """
        return (
            f"'{self._name}', Price: ${self._price:.2f}, "  # @format
            f"Quantity: {self.quantity}, Maximum: {self.maximum}"
        )

    def buy(self, quantity: int) -> float:
        """
        Checks the quantity of the product, checks the maximum quantity.
        Buys a given quantity below or equal maximum of the product.
        Returns the total price of the purchase. (float)
        """
        if int(quantity) <= 0:
            raise ValueError("argument 'quantity' must be >= 1 to buy a product")
        if self.maximum < quantity:
            raise MaximumValueError(self._name, self.maximum)
        if (self._quantity - int(quantity)) < 0:
            raise OutOfStockValueError(self._name, quantity)
        self.quantity -= int(quantity)
        return float(quantity) * self._price


if __name__ == "__main__":
    non_stocked = NonStockedProduct("Mac License", 150.00)
    print(non_stocked.show())

    limited = LimitedProduct("Shipping fee", 9.95, 500, 1)
    print(limited.show())
    limited.buy(2)


# - eof -
