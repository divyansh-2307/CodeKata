from CodeKata.apps.checkout.cart import Cart
from CodeKata.db_models.ck_products import CkProducts

class Checkout:
    def __init__(self):
        self.cart = Cart()
        self.ck_products = CkProducts()
        self.product_details = self.get_product_details()

    def get_product_details(self):
        """
        initialize products and offers
        :return: product_details
        """
        product_details_db = self.ck_products.get_all_product_and_offers()
        # format the product_details
        product_details = {}

        for product in product_details_db:
            name = product['name']
            if name not in product_details:
                product_details[name] = {'price': product['price'], 'offers': []}
            if product['offer_price'] is not None and product['quantity'] is not None:
                product_details[name]['offers'].append(
                    {'offer_price': product['offer_price'], 'quantity': product['quantity']})

        # sort the offers based on price/quantity ratio
        for product in product_details.values():
            product['offers'].sort(key=lambda x: x['offer_price'] / x['quantity'])
        return product_details

    def scan_item(self, product):
        """
        Method to add product to cart
        :param product_name:
        :return:
        """

        # validate if correct product name is provided
        if product not in self.product_details:
            return dict(success=False, error="Invalid product name provided")
        else:
            self.cart.add_product(product)
        return dict(success=True)

    def calculate_cart_value(self):
        """
        Method to calculate the total current cart value
        :param
        :return: cart value
        """
        cart_amount = 0

        # Iterate through each item and its frequency
        for product, frequency in self.cart.get_cart_products().items():
            curr_frequency = frequency
            offer_index = 0
            offer_details = self.product_details[product].get("offers", [])
            offer_length = len(offer_details)
            # iterate through offers checking if quantity is applicable or not, sorted based on lowest price value
            # if a favourable offer is found, deduct its frequency and add its value
            while (curr_frequency > 0 and offer_index < offer_length):
                if curr_frequency >= offer_details[offer_index]["quantity"]:
                    cart_amount += (offer_details[offer_index]["offer_price"]) * (
                                curr_frequency // offer_details[offer_index]["quantity"])
                    curr_frequency %= offer_details[offer_index]["quantity"]
                else:
                    # if offer conditions are not favourable, move to next best offer
                    offer_index += 1

            # if there are no offers, or offers are exhausted, add default item prices
            if curr_frequency > 0:
                cart_amount += curr_frequency * self.product_details[product]["price"]
        return cart_amount


