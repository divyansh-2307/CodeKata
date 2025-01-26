--------------------------------------------:Checkout Kata:----------------------------------------------------------

Problem Statement:

Implement the code for a supermarket checkout process that calculates the total
price of items added in the cart by the customer. In our store, we’ll use individual
letters of the alphabet (A, B, C, and so on) to represent items. Products can be
purchased at their individual pricing or at a discounted price when purchased in
groups as listed below: For example, item ‘A’ might cost 50 cents individually, but
this week we have a special offer: buy three ‘A’s and they’ll cost you $1.30. Product
pricing for this week is as below::

Item    Unit    Special
        Price   Price
----------------------
  A      50     3 for 150
  B      30     2 for 45
  C      20
  D      15

Our checkout accepts items in any order, so that if we scan product B, then product
A, and then another product B, we’ll recognize the two B’s and price them at a
discounted price of Rs 45 instead of individual pricing of Rs 30, which brings the
Total order pricing to Rs 95.


---------------------------------------------:ABOUT:-----------------------------------------------------------------
CodeKata is a Django-based project designed to manage a supermarket checkout store.


---------------------------------------------:FEATURES:---------------------------------------------------------------
- Manage Product and their offers.
- Multiple offer utility over same product.
- Automatic checkout price optimization based on selection and active offers.
- Scalable and maintainable backend.


-----------------------------------------:SETUP INSTRUCTIONS:---------------------------------------------------------
Step 1: Clone the Repository

    git clone <repository-url>
    cd CodeKata


Step 2: Create a Virtual Environment

    python -m venv venv
    source venv/bin/activate


Step 3: Install Dependencies

    pip install -r requirements.txt


Step 4: Update Environment Settings

    Add your database connection details in CodeKata/settings/dev.py


Step 5: Apply Migrations

    python manage.py makemigrations db_models
    python manage.py migrate


-----------------------------------------:CUSTOMIZATIONS:---------------------------------------------------------

The current configuration of products and offer is set as per the provided assignment questionnaire

For custom test cases:
proceed to: CodeKata/apps/products/app_settings.py
Update PRODUCT_PRICE_MAPPING for updating the product pricing
Update PRODUCT_OFFER_MAPPING for updating the product offers


----------------------------------------:INITIALIZATION & OPERATION:-----------------------------------------------
Proceed to initialize_project.py file
and run the __main__ method by following instruction for processing cart and custom input

process_cart  -----> Direct string approach
process_cart_v2 ---> iteratively product addition and cart value approach
