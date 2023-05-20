import pymysql
import mysql.connector
from datetime import date, datetime


class ItemDatabase:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="@27September2000",
            database="medical_records"
        )
        self.cursor = self.mydb.cursor()

    def get_kpi(self, mail):
        query = f"SELECT * FROM kpi_table WHERE email = '{mail}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def create_kpi(self, mail, total_sale_and_marketing, total_revenue, total_cust, user_stopped, cogs):
        # if email exists in the table, then sum the values of total_sale_and_marketing, total_revenue, total_cust, user_stopped, cogs
        # else create a new row
        query = f"SELECT * FROM kpi_table WHERE email = '{mail}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result) == 0:
            query = f"INSERT INTO kpi_table (email, total_sale_and_marketing, total_revenue, total_cust, user_stopped, cogs) VALUES ('{mail}', {total_sale_and_marketing}, {total_revenue}, {total_cust}, {user_stopped}, {cogs})"
            self.cursor.execute(query)
            self.mydb.commit()
            return "successfully created"
        else:
            query = f"UPDATE kpi_table SET total_sale_and_marketing = total_sale_and_marketing + {total_sale_and_marketing}, total_revenue = total_revenue + {total_revenue}, total_cust = total_cust + {total_cust}, user_stopped = user_stopped + {user_stopped}, cogs = cogs + {cogs} WHERE email = '{mail}'"
            self.cursor.execute(query)
            self.mydb.commit()
            return "successfully updated"
