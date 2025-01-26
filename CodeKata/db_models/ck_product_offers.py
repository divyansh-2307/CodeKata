import uuid
from CodeKata.utils.mysql_helper import MySQLHelper


class CkProductOffers:
    def __init__(self, **kwargs):
        self.database = "codekata"
        self.table_name = "ck_product_offers"
        self.db_helper = MySQLHelper()

    def insert_offer(self, offer_entity):
        inserted_id = self.db_helper.insert(self.table_name, offer_entity)
        return inserted_id

    def insert_multiple_offers(self, offers_list: list):
        row_count = self.db_helper.insert_multiple(self.table_name, offers_list)
        return row_count

    def truncate_table(self):
        query = f"TRUNCATE TABLE {self.table_name}"
        self.db_helper.query(query)

    def fetch_offer_by_product_names(self, products_name: list):
        query = f"""SELECT p.name, o.quantity, o.offer_price from {self.table_name} o JOIN ck_products p 
                    ON p.unique_id = o.product_unique_id WHERE p.active = 1 and o.active = 1 and 
                    o.expiry_date > CURDATE() and p.name in ({ ', '.join(['%s'] * len(products_name))})"""
        return self.db_helper.query(query, products_name)


