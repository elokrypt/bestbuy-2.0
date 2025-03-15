"""
Unit Tests for the Product-class.
"""

import pytest

from products import Product, OutOfStockValueError


def test_creating_prod():
    assert isinstance(
        Product(name="AMD Ryzen 57000X", price=150.00, quantity=25), Product
    )


def test_creating_prod_invalid_details():
    with pytest.raises(ValueError, match="argument 'name' is an empty string"):
        # Empty name
        Product("", price=1450, quantity=100)
    with pytest.raises(ValueError, match="argument 'price' is negative."):
        # Negative Price
        Product("MacBook Air M2", price=-10, quantity=100)
    with pytest.raises(ValueError, match="argument 'quantity' is negative."):
        # Negative Quantity
        Product("MacBook Air M2", price=10.0, quantity=-100)
    with pytest.raises(ValueError, match="argument 'quantity' is negative."):
        # Negative quantity setter value
        Product("MacBook Air M2", price=10.0, quantity=100).quantity = -1


def test_prod_becomes_inactive():
    product = Product(name="AMD Ryzen 57000X", price=150.00, quantity=5)
    # check instance and if product is active via method
    assert isinstance(product, Product) and product.is_active()
    # set quantity to zero via setter
    product.quantity = 0
    # check active via getter and method
    assert not product.active and not product.is_active()


def test_buy_modifies_quantity():
    product = Product(name="AMD Ryzen 57000X", price=150.00, quantity=5)
    # check instance and product quantity via getter
    assert isinstance(product, Product) and product.quantity == 5
    # purchase 2x item from product, expect price of 2 * 150.00
    assert product.buy(2) == 300.00
    # check quantity via getter
    assert product.quantity


def test_buy_too_much():
    product = Product(name="AMD Ryzen 57000X", price=150.00, quantity=5)
    # check instance and product quantity via getter
    assert isinstance(product, Product) and product.quantity == 5
    with pytest.raises(
        OutOfStockValueError,
        match="store cannot provide 7x 'AMD Ryzen 57000X'",
    ):
        # buy more than available items.
        product.buy(7)


test_creating_prod()
test_creating_prod_invalid_details()
test_prod_becomes_inactive()
test_buy_modifies_quantity()
test_buy_too_much()
