#  -*- coding: utf-8 -*-
#  @filename main.py
#  @author Marcel Bobolz
#  @last_modified 2025-03-14T23:40:51.028Z
"""
Implements the Best Buy - Store CLI.
"""

from typing import List, Tuple

from products import Product, OutOfStockError
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
        print(f"{lino}. {product.show()}")
    print("""-----
    """)


def start(store: Store):
    """
    CLI implementation for the "Best Buy" store.
    """
    do_quit = False
    while not do_quit:
        products: List[Product] = store.get_all_products()
        try:
            choice = int(input(STORE_MENU))
        except ValueError:
            print("Error with your choice! Try again!")
        match choice:
            case 1:
                show_all_products(products)
            case 2:
                print(f"\nTotal of {store.get_total_quantity()} items in store\n")
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
                        prod_qty = int(prod_qty)
                        order = (products[prod_index], prod_qty)
                        shopping_list.append(order)
                        print("\nProduct added to list!\n")
                    except ValueError:
                        print("\n- Error adding product ! -\n")
                if len(shopping_list) > 0:
                    try:
                        total_price = store.order(shopping_list)
                        print(f"********\nOrder made! Total payment ${total_price:.2f}")
                    except OutOfStockError:
                        print("Error while making order! Quantity larger than what exists.")
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
    ]
    best_buy = Store(product_list)
    try:
        start(best_buy)
    except KeyboardInterrupt:
        print("\nCTRL-C catched -> Exiting...")


if __name__ == "__main__":
    main()
