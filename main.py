#  -*- coding: utf-8 -*-
#  @filename main.py
#  @author Marcel Bobolz
"""
Implements the Best Buy - Store CLI.
"""

from typing import List, Tuple

from products import Product, NonStockedProduct, LimitedProduct
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree
from store import Store, ProductOrder

STORE_MENU = """
   Store Menu
   ----------
1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit
Please choose a number: """


def show_all_products(products: List[Product]):
    """
    Prints out all products in a list of products.
    """
    lino = 0
    print("\n-----")
    for product in products:
        lino += 1
        print(f"{lino}. {product}")
    print("""-----
    """)


def start(store: Store):
    """
    CLI implementation for the "Best Buy" store.
    """
    do_quit = False
    while not do_quit:
        products: List[Product] = store.get_all_products()
        products_len: int = len(products)
        try:
            choice = int(input(STORE_MENU))
        except ValueError:
            print("Error with your choice! Try again!")
        match choice:
            case 1:
                show_all_products(products)
            case 2:
                print(
                    f"\nTotal of {store.get_total_quantity()} items in store\n"
                )
            case 3:
                prod_num: str | int
                prod_qty: str | int
                order: ProductOrder
                shopping_list: List[Tuple[Product, int]] = []
                show_all_products(products)
                print("When you want to finish order, enter empty text.")
                while True:
                    prod_num = input("Which product # do you want? ")
                    prod_qty = input("What amount do you want? ")
                    if len(prod_num) == 0 or len(prod_qty) == 0:
                        break
                    try:
                        prod_index = int(prod_num) - 1
                        if prod_index >= products_len or prod_index < 0:
                            raise IndexError
                        prod_qty = int(prod_qty)
                        if prod_qty <= 0:
                            raise ValueError
                        order = (products[prod_index], prod_qty)
                        shopping_list.append(order)
                        print("\nProduct added to list!\n")
                    except IndexError:
                        print("\n- Product-Index # out of bounds ! - \n")
                    except ValueError:
                        print("\n- Error adding product ! -\n")
                if len(shopping_list) > 0:
                    try:
                        total_price = store.order(shopping_list)
                        print(
                            f"********\n"
                            f"Order made! Total payment ${total_price:.2f}"
                        )
                    except ValueError as e:
                        print(f"Error:\n\t{e.message}")
            case 4:
                do_quit = True
        continue


def main():
    """
    Main function.
    """
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% Off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = Store(product_list)
    try:
        start(best_buy)
    except KeyboardInterrupt:
        print("\nCTRL-C catched -> Exiting...")


""" def test_store_operators():
    prod_list_1 = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
    ]

    prod_list_2 = [
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    print("Testing '<' operator (should return True)")
    print(f"Result: {prod_list_1[1] < prod_list_1[2]}")

    print("Testing '>' operator (should return True)")
    print(f"Result: {prod_list_1[2] > prod_list_1[1]}")

    store_a = Store(prod_list_1)
    store_b = Store(prod_list_2)

    print("Testing 'in' operator (should return True)")
    print(f"Result: {prod_list_1[1] in store_a}")

    best_buy = store_a + store_b

    start(best_buy) """


if __name__ == "__main__":
    # test_store_operators()
    main()

# - eof -
