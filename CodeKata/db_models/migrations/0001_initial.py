from django.db import migrations, connection


def initialize_database(apps, schema_editor):
    with connection.cursor() as cursor:
        # Create schema if it doesn't exist
        cursor.execute("CREATE SCHEMA IF NOT EXISTS codekata")

        # Switch to the schema
        cursor.execute("USE codekata")

        # Create ck_products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ck_products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                unique_id VARCHAR(64) NOT NULL UNIQUE,
                name VARCHAR(128) NOT NULL,
                product_id VARCHAR(64) NOT NULL,
                price INT NOT NULL,
                category VARCHAR(64) NOT NULL,
                company VARCHAR(64) NOT NULL,
                ct DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                ut DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                active TINYINT(1) NOT NULL DEFAULT 1
            )
        """)

        # Create ck_product_offers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ck_product_offers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                unique_id VARCHAR(64) NOT NULL UNIQUE,
                product_unique_id VARCHAR(64) NOT NULL,
                quantity INT NOT NULL,
                offer_price INT NOT NULL,
                expiry_date DATE NOT NULL DEFAULT '2026-01-01',
                ct DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                ut DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                active TINYINT(1) NOT NULL DEFAULT 1
            )
        """)


class Migration(migrations.Migration):
    # Define dependencies (empty for the initial migration)
    dependencies = []

    # Define the operations to run
    operations = [
        migrations.RunPython(initialize_database),
    ]
