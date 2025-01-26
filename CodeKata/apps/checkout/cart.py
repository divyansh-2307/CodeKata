class Cart:
    def __init__(self):
        self.cart_products = {}

    def add_product(self, product):
        """
        Method to Add product in cart
        :return:
        """
        if product in self.cart_products:
            self.cart_products[product] += 1
        else:
            self.cart_products[product] = 1

    def get_cart_products(self):
        """
        Method to get products and quantity in cart
        :return:
        """
        return self.cart_products