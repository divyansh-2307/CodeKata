import uuid

from CodeKata.utils.mysql_helper import MySQLHelper


class CkProducts:
    def __init__(self, **kwargs):
        self.database = "codekata"
        self.table_name = "ck_products"
        self.db_helper = MySQLHelper()

    def insert_product(self, product_entity):
        inserted_id = self.db_helper.insert(self.table_name, product_entity)
        return inserted_id

    def insert_multiple_products(self, products_list: list):
        row_count = self.db_helper.insert_multiple(self.table_name, products_list)
        return row_count

    def truncate_table(self):
        query = f"TRUNCATE TABLE {self.table_name}"
        self.db_helper.query(query)

    def fetch_products_by_name(self, unique_products_on_offer: list):
        query = f"SELECT unique_id, name, price from {self.table_name} where name in ({ ', '.join(['%s'] * len(unique_products_on_offer))}) and active = 1"
        return self.db_helper.query(query, unique_products_on_offer)

    def get_all_product_and_offers(self):
        query = f"""SELECT p.name, p.price, o.quantity, o.offer_price from {self.table_name} p  LEFT JOIN ck_product_offers o on p.unique_id = o.product_unique_id 
                    WHERE p.active = 1 and (o.active = 1 AND o.expiry_date > CURDATE() OR o.product_unique_id IS NULL)"""
        return self.db_helper.query(query)
