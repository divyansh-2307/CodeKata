import http
from collections import Counter, defaultdict
from math import remainder, floor

from CodeKata.db_models.ck_products import CkProducts
from CodeKata.db_models.ck_product_offers import CkProductOffers


def cart_checkout(request_body):
    """
    Method to evaluate the checkout cart price, based on the provided cart string where each alphabet denotes a product
    :param request_body: {"cart": "ABCDEFGHIJK"}
    :return: total value of cart, {"cart_value": 120}
    """
    cart = request_body.get("cart")
    if cart is None or len(cart) == 0:
        return dict(status_code=http.HTTPStatus.OK, success=True, data={"cart_value": 0})

    # create map of distinct products in cart with there frequency
    product_frequency = Counter(cart)

    # check if the products are valid of not
    product_details = CkProducts().fetch_products_by_name(list(product_frequency.keys()))
    if product_details is None or len(product_frequency.keys()) != len(product_details):
        return dict(statuc_code=http.HTTPStatus.BAD_REQUEST, success=False, details_message="Invalid products provided.")

    # fetch product price
    product_name_price_map = {x["name"]: x["price"] for x in product_details}

    # fetch relevant offers on the products which are active and valid
    products_offer_db = CkProductOffers().fetch_offer_by_product_names(list(product_frequency.keys()))
    product_offers = {}

    for product in products_offer_db:
        name = product['name']
        if name not in product_offers:
            product_offers[name] = []
        product_offers[name].append(product)

    # Sort each product offers based on the offer_price / quantity ratio
    for name in product_offers:
        product_offers[name] = sorted(product_offers[name], key=lambda x: x['offer_price'] / x['quantity'])

    # evaluate cart
    cart_amount = 0

    # Iterate through each item and its frequency
    for product, frequency in product_frequency.items():
        # check offers available on product and quantity
        curr_frequency = frequency
        offer_index = 0
        offer_length = len(product_offers.get(product, []))
        # iterate through offers checking if quantity is applicable or not, sorted based on lowest price value
        # if a favourable offer is found, deduct its frequency and add its value
        while(curr_frequency > 0 and offer_index < offer_length):
            if curr_frequency >= product_offers[product][offer_index]["quantity"]:
                cart_amount += (product_offers[product][offer_index]["offer_price"])*(curr_frequency//product_offers[product][offer_index]["quantity"])
                curr_frequency %= product_offers[product][offer_index]["quantity"]
            else:
                # if offer conditions are not favourable, move to next best offer
                offer_index += 1

        # if there are no offers, or offers are exhausted, add default item prices
        if curr_frequency > 0:
            cart_amount += curr_frequency*product_name_price_map[product]

    return dict(status_code=http.HTTPStatus.OK, success=True, data={"cart_value": int(cart_amount)})