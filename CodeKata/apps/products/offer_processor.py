from CodeKata.apps.products.app_settings import PRODUCT_OFFER_MAPPING
from CodeKata.db_models.ck_product_offers import CkProductOffers
from CodeKata.db_models.ck_products import CkProducts
import uuid

def initialise_offers():
    """
    Method to initialize the offers for products
    :return:
    """
    if len(PRODUCT_OFFER_MAPPING[0]) != len(PRODUCT_OFFER_MAPPING[1]) or len(PRODUCT_OFFER_MAPPING[2]) != len(PRODUCT_OFFER_MAPPING[1]):
        return dict(success=False, error="Improperly configured PRODUCT_OFFER_MAPPING")

    # truncate the table ck_products
    CkProductOffers().truncate_table()

    unique_products_on_offer = list(set(PRODUCT_OFFER_MAPPING[0]))
    product_name_id_details = CkProducts().fetch_products_by_name(unique_products_on_offer)
    if len(product_name_id_details) != len(unique_products_on_offer):
        return dict(success=False, error="Improperly configured PRODUCT_OFFER_MAPPING, invalid product names")

    product_name_id_map = {x["name"]: x["unique_id"] for x in product_name_id_details}
    product_name_price_map = {x["name"]: x["price"] for x in product_name_id_details}

    # add new entities
    product_entities = []
    for i in range(0, len(PRODUCT_OFFER_MAPPING[0])):
        name = PRODUCT_OFFER_MAPPING[0][i]
        quantity = PRODUCT_OFFER_MAPPING[1][i]
        offer_price = PRODUCT_OFFER_MAPPING[2][i]
        if offer_price/quantity >= product_name_price_map[name]:
            return dict(success=False, error=f"Invalid offer configured for product: {name}, offer value should not be greater than net indivisual value.")
        product_entity = {
            "unique_id": uuid.uuid4().hex,
            "product_unique_id": product_name_id_map[name],
            "quantity": quantity,
            "offer_price": offer_price,
            "active": 1
        }
        product_entities.append(product_entity)

    # insert new products
    row_count = CkProductOffers().insert_multiple_offers(product_entities)

    if row_count == len(PRODUCT_OFFER_MAPPING[0]):
        return dict(success=True)
    return dict(success=False)