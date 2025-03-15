#  -*- coding: utf-8 -*-
#  @filename promotions.py
#  @author Marcel Bobolz
#  @last_modified 2025-03-15T12:34:08.513Z
"""
Implementation of Promotion abtract class,
and SecondHalfPrice, ThirdOneFree + PercentDiscount class interfaces.
"""

from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    Implements the abstract Promotion class.
    """

    def __init__(self, name: str):
        """
        Initializes the Promotion.
        """
        if len(name) == 0:
            raise ValueError("argument 'name' is an empty string.")
        self.name = name

    def __str__(self) -> str:
        return f"'{self.name}'"

    @abstractmethod
    def apply_promotion(self, product: object, quantity: int) -> float:
        """
        Applies the promotion onto the 'product' with given 'quantity'.
        Returns the discounted price as float.
        """
        pass


class SecondHalfPrice(Promotion):
    """
    Implements the SecondHalfPrice -class-interface.
    """

    def apply_promotion(self, product: object, quantity: int) -> float:
        """
        Apply the 'half-price' discount onto 'quantity' of 'product'.
        Returns the final price as float.
        """
        half_qty: int = quantity - int(quantity // 2)
        half_price: float = product.price / 2
        total_price: float = half_qty * half_price
        +(half_qty * product.price)
        return total_price


class ThirdOneFree(Promotion):
    """
    Implements the ThirdOneFree -class-interface.
    """

    def apply_promotion(self, product: object, quantity: int) -> float:
        """
        Apply the 'third-one-free' discount onto 'quantity'
        of 'product'.
        Returns the final price as float.
        """
        tertiar_qty: int = int(quantity // 3)
        total_price: float = (quantity - tertiar_qty) * product.price
        return total_price


class PercentDiscount(Promotion):
    """
    Implements the PercentDiscount -class-interface.
    """

    def __init__(self, name: str, percent: float | int):
        """
        Initializes a PercentDiscount instance.
        """
        super().__init__(name=name)
        if float(percent) <= 0.00:
            raise ValueError("argument 'percent' is negative or zero.")
        self.percent = float(percent)

    def apply_promotion(self, product: object, quantity: int) -> float:
        """
        Apply the 'percent' discount onto 'quantity' of 'product'.
        Returns the final price as float.
        """
        discount_price = product.price
        -(product.price * (self.percent * 0.01))
        return discount_price * quantity


# - eof -
