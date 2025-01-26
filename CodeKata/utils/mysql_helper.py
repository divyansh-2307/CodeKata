import pymysql
from django.conf import settings


class MySQLHelper:
    def __init__(self):
        self.db_config = settings.DATABASES["default"]

    def _connect(self):
        return pymysql.connect(
            host=self.db_config["HOST"],
            user=self.db_config["USER"],
            password=self.db_config["PASSWORD"],
            database=self.db_config["NAME"],
            port=int(self.db_config["PORT"]),
            charset="utf8mb4",
        )

    def query(self, query, params=None):
        try:
            conn = self._connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            return rows
        except pymysql.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()

    def insert(self, table_name, data):
        try:
            conn = self._connect()
            cursor = conn.cursor()

            # Build the query dynamically
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            cursor.execute(query, tuple(data.values()))
            conn.commit()
            return cursor.lastrowid
        except pymysql.Error as e:
            print(f"Error inserting data: {e}")
            return None
        finally:
            conn.close()

    def insert_multiple(self, table_name, data_list):
        try:
            conn = self._connect()
            cursor = conn.cursor()

            columns = ", ".join(data_list[0].keys())
            placeholders = ", ".join(["%s"] * len(data_list[0]))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            values = [tuple(data.values()) for data in data_list]
            cursor.executemany(query, values)
            conn.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            print(f"Error inserting multiple rows: {e}")
            return None
        finally:
            conn.close()