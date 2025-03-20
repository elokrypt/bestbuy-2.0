#  -*- coding: utf-8 -*-
#  @filename products.py
#  @author Marcel Bobolz
#  @last_modified 2025-03-15T12:40:03.733Z
"""
Implementation of Product class interface, plus OutOfStockError
and NonStockedProduct + LimitedProduct subclasses
"""

from abc import ABC, abstractmethod

from promotions import Promotion


class MaximumValueError(Exception):
    """
    Exception raised for maximum-value per order edge-cases.
    """

    def __init__(self, name, maximum):
        self.message = f"store provides max. {maximum}x '{name}' per order"
        super().__init__(self.message)


class OutOfStockValueError(Exception):
    """
    Exception raised for Out-Of-Stock scenarios
    """

    def __init__(self, name, quantity):
        self.message = f"store cannot provide {quantity}x '{name}'"
        super().__init__(self.message)


class BaseProduct(ABC):
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
            raise ValueError("argument 'name' is an empty string.")
        self._name = name
        if float(price) < 0.00:
            raise ValueError("argument 'price' is negative.")
        self._price = float(price)
        if int(quantity) < 0:
            raise ValueError("argument 'quantity' is negative.")
        self.quantity = int(quantity)
        self.promotion = None

    @property
    def name(self) -> str:
        """
        Getter for product-name.
        """
        return self._name

    @property
    def price(self) -> float:
        """
        Getter for product-price.
        """
        return self._price

    @property
    def quantity(self) -> float:
        """
        Getter for product-quantity.
        """
        return float(self._quantity)

    @quantity.setter
    def quantity(self, quantity: int):
        """
        Setter for product-quantity.
        """
        if quantity < 0:
            raise ValueError("argument 'quantity' is negative.")
        if quantity < 1:
            self.deactivate()
        self._quantity = quantity

    @property
    def promotion(self) -> Promotion | None:
        """
        Getter for any active promotion.
        Returns active Promotion instance or None.
        """
        return self._promotion

    @promotion.setter
    def promotion(self, promotion: Promotion | None):
        """
        Setter for activivating a Promotion.
        Sets the active Promotion instance.
        """
        self._promotion = promotion

    @promotion.deleter
    def promotion(self):
        self.promotion = None

    def set_promotion(self, promotion: Promotion):
        """
        Method for activivating a Promotion.
        Sets the active Promotion instance.
        """
        self.promotion = promotion

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
        return (
            f"'{self.name}', Price: ${self.price:.2f}, "
            f"Quantity: {self.quantity}, "
            f"Promotion: {self.promotion}"
        )

    def buy(self, quantity: int) -> float:
        """
        Checks the quantity, if inside available boundaries.
        Updates the quantity of the product.
        Returns the total price (float) of the purchase.
        """
        if int(quantity) <= 0:
            raise ValueError(
                "argument 'quantity' must be >= 1 to buy a product"
            )
        if (self.quantity - int(quantity)) < 0:
            raise OutOfStockValueError(self._name, quantity)
        self.quantity -= int(quantity)

        if self.promotion is not None:
            return self.promotion.apply_promotion(self, quantity)
        else:
            return float(quantity) * self.price


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
    def quantity(self) -> float:
        """
        Getter for quantity (=0 -> see class description)
        """
        return float(self._quantity)

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
        return (
            f"'{self.name}', Price: ${self.price:.2f}, "
            f"Quantity: Unlimited, "
            f"Promotion: {self.promotion}"
        )

    def buy(self, quantity: int) -> float:
        """
        Buys a given quantity of the product.
        """
        if int(quantity) <= 0:
            raise ValueError(
                "argument 'quantity' must be >= 1 to buy a product"
            )

        if self.promotion is not None:
            return self.promotion.apply_promotion(self, quantity)
        else:
            return float(quantity) * self.price


class LimitedProduct(Product):
    """
    Some products can only be purchased X times in an order.
    For example - a shipping fee can only be added once.
    If an order is attempted with quantity larger than the 'maximum' one,
    it should be refused with an 'OrderLimitedError' exception.
    """

    def __init__(
        self, name: str, price: float | int, quantity: int, maximum: int
    ):
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
            f"'{self.name}', Price: ${self.price:.2f}, "
            f"Limited to {self.maximum} per order!, "
            f"Promotion: {self.promotion}"
        )

    def buy(self, quantity: int) -> float:
        """
        Checks the quantity of the product, checks the maximum quantity.
        Buys a given quantity below or equal maximum of the product.
        Returns the total price of the purchase. (float)
        """
        if int(quantity) <= 0:
            raise ValueError(
                "argument 'quantity' must be >= 1 to buy a product"
            )
        if self.maximum < quantity:
            raise MaximumValueError(self.name, self.maximum)
        if (self.quantity - int(quantity)) < 0:
            raise OutOfStockValueError(self.name, quantity)
        self.quantity -= int(quantity)

        if self.promotion is not None:
            return self.promotion.apply_promotion(self, quantity)
        else:
            return float(quantity) * self.price


# - eof -
