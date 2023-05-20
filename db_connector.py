import pymysql
import mysql.connector
from datetime import date, datetime


class ItemDatabase:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="@27September2000",
            database="Finnit"
        )
        self.cursor = self.mydb.cursor()

    def get_kpi(self, mail):
        query = f"SELECT * FROM kpi_table WHERE email = '{mail}'"
        self.cursor.execute(query)
        startup = {}
        for row in self.cursor.fetchall():
            mail = row[0]
            total_sale_and_marketing = row[1]
            total_revenue = row[2]
            total_customer = row[3]
            user_stopped = row[4]
            cogs = row[5]

        kpi = {}

        if(total_customer== None):
            kpi["cac"] = None
            kpi["churn_rate"] = None
            avg_rpc = None
            kpi["clv"] = None

        if(total_sale_and_marketing == None):
            kpi["cac"] = None
        else:
            kpi["cac"] = total_sale_and_marketing/total_customer
        
        if(user_stopped == None):
            kpi["churn_rate"] = None
            kpi["clv"] = None
        else:
            kpi["churn_rate"] = user_stopped/total_customer

        if(total_revenue==None):
            avg_rpc = None
            kpi["gross_margin"] = None
            kpi["clv"] = None
        else:
            kpi["gross_margin"] = (total_revenue-cogs)/(total_revenue*100)
            avg_rpc = total_revenue/total_customer

        if(avg_rpc!=None and kpi["churn_rate"]!=None):
            kpi["clv"] = avg_rpc/kpi["churn_rate"]

        return [kpi]

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
