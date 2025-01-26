import os

from CodeKata.apps.checkout.checkout import Checkout
from CodeKata.apps.products.offer_processor import initialise_offers
from CodeKata.apps.products.product_processor import initialise_products
from CodeKata.apps.checkout.checkout_processor import cart_checkout

def initialize_db():
    """
    Method to initialize db for Products, Prices and offer based on configuration fetched from CodeKata/apps/products/app_settings.py
    :return:
    """
    print("Initializing Products...")
    product_init_resp = initialise_products()
    if not product_init_resp.get("success", False):
        print(f"Error while Initializing Products: {product_init_resp.get('error', '')} \n")
        return
    print("Products Initialization success... \n")

    print("Initializing offers...")
    offer_init_resp = initialise_offers()
    if not offer_init_resp.get("success", False):
        print(f"Error while Initializing Product offers: {offer_init_resp.get('error', '')} \n")
        return
    print("Product Offers Initialization success... \n")


def process_cart(cart: str):
    """
    Method to process checkout cart and print value
    :param cart:
    :return:
    """
    checkout_resp = cart_checkout({"cart": cart})
    if not checkout_resp.get("success", False):
        print(f"Cart Checkout Error: {checkout_resp['details_message']['cart_value']} \n")
    print(f"CART: {cart}    VALUE: {checkout_resp['data']['cart_value']} \n")


def process_cart_v2(cart: str):
    """
    Method to iteratively add items to cart and print the cart value as items increase and offers apply
    :param cart:
    :return:
    """
    checkout = Checkout()
    for i  in range(0, len(cart)):
        scan_resp = checkout.scan_item(cart[i])
        if not scan_resp.get("success", False):
            print(f"Error: Invalid product {cart[i]} in Cart. \n")
            break
        print(f"CART: {cart[:i+1]}    AMOUNT: {checkout.calculate_cart_value()}")


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeKata.settings.dev')
    environment = os.getenv('DJANGO_ENV', 'dev')
    os.environ['DJANGO_SETTINGS_MODULE'] = f'CodeKata.settings.{environment}'

    # initialize db with offers
    # Note: comment after initialization if the product and offer configuration are same.
    # initialize_db()

    # enter your test CART below
    cart = "AAAAA"

    # process cart 1
    # process_cart(cart)

    # process cart 2
    process_cart_v2(cart)
