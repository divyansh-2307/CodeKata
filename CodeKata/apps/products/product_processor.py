import http
import json
import uuid

from django.contrib.messages import success

from CodeKata.db_models.ck_products import CkProducts
from CodeKata.apps.products.app_settings import PRODUCT_PRICE_MAPPING


def add_new_product(data):
    """
    Method to add new products within the database
    :param data: {"product_name": "", "category": "", "price": "", "product_id": "", "company": ""}
    :return:
    """
    product_name = data.get("product_name")
    category = data.get("category")
    price = data.get("price")
    product_id = data.get("product_id")
    company = data.get("company")

    # validate input parameters
    if product_name is None or category is None or price is None or product_id is None or company is None:
        return dict(status_code=http.HTTPStatus.BAD_REQUEST, success=False,
                    details_message="Incomplete request body.")
    if category not in ["FOOD", "BEVERAGE", "SANITARY"]:
        return dict(status_code=http.HTTPStatus.BAD_REQUEST, success=False,
                    details_message="Invalid category selected.")
    if not isinstance(price, int):
        return dict(status_code=http.HTTPStatus.BAD_REQUEST, success=False,
                    details_message="Invalid price provided.")

    unique_id = uuid.uuid4().hex

    # add this to database
    product_entity = {
        "unique_id": unique_id,
        "name": product_name,
        "price": price,
        "product_id": product_id,
        "category": category,
        "company": company,
        "active": 1
    }
    row_id = CkProducts().insert_product(product_entity)
    if row_id is None or row_id < 0:
        return dict(status_code=http.HTTPStatus.BAD_REQUEST, success=False,
                    details_message="Error while adding new product.")

    return dict(status_code=http.HTTPStatus.OK, success=True, data={"unique_id": unique_id})


def initialise_products():
    """
    Method to initialize the products based on the given assignment.
    :return:
    """
    if len(PRODUCT_PRICE_MAPPING[0]) != len(PRODUCT_PRICE_MAPPING[1]):
        return dict(success=False, error="Improperly configured PRODUCT_PRICE_MAPPING")

    # truncate the table ck_products
    CkProducts().truncate_table()

    # add new entities
    product_entities = []
    for i in range(0, len(PRODUCT_PRICE_MAPPING[0])):
        product_entity = {
            "unique_id": uuid.uuid4().hex,
            "name": PRODUCT_PRICE_MAPPING[0][i],
            "price": PRODUCT_PRICE_MAPPING[1][i],
            "product_id": PRODUCT_PRICE_MAPPING[0][i],
            "category": "FOOD",
            "company": "xyz",
            "active": 1
        }
        product_entities.append(product_entity)

    # insert new products
    row_count = CkProducts().insert_multiple_products(product_entities)

    if row_count == len(PRODUCT_PRICE_MAPPING[0]):
        return dict(success=True)
    return dict(success=False, error="Error while inserting data insertion")







