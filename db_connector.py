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
            kpi["avg_rpc"] = None
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
            kpi["avg_rpc"] = None
            kpi["gross_margin"] = None
            kpi["clv"] = None
        else:
            kpi["gross_margin"] = (total_revenue-cogs)/(total_revenue*100)
            kpi["avg_rpc"] = total_revenue/total_customer

        if(kpi["avg_rpc"]!=None and kpi["churn_rate"]!=None):
            kpi["clv"] = kpi["avg_rpc"]/kpi["churn_rate"]

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
        

    def create_burn(self, mail, salaries, miscellaneous, marketing, operation, cogs, investment, bootstrap, revenue):
        outflow = salaries + miscellaneous + marketing + operation + cogs
        inflow = revenue
        query = f"SELECT * FROM burn_rate WHERE email = '{mail}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result) == 0:
            query = f"INSERT INTO burn_rate (email, salaries, miscellaneous, marketing, operations, cogs, cash_outflow, investment, bootstrap, revenue, cash_inflow) VALUES ('{mail}', {salaries}, {miscellaneous}, {marketing}, {operation}, {cogs}, {outflow}, {investment}, {bootstrap}, {revenue}, {inflow})"
            self.cursor.execute(query)
            self.mydb.commit()
            return "successfully created"
        else:
            query = f"UPDATE burn_rate SET salaries = {salaries}, miscellaneous = {miscellaneous}, marketing =  {marketing}, operations = {operation}, cogs = {cogs}, cash_outflow = {outflow}, investment = {investment}, bootstrap = {bootstrap}, revenue = {revenue}, cash_inflow = {inflow} WHERE email = '{mail}'"
            self.cursor.execute(query)
            self.mydb.commit()
            return "successfully updated"

    def get_burn(self, mail):
        query = f"SELECT * FROM burn_rate WHERE email = '{mail}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            mail = row[0]
            outflow = row[6]
            investment = row[7]
            bootstrap = row[8]
            inflow = row[10]
        
        net_burnrate = outflow - inflow
        cash_left = investment + bootstrap - net_burnrate
        burnrate={}
        burnrate["time_in_months"] = cash_left/net_burnrate
        return [burnrate]
    
    def create_break(self, mail, fixed_cost, variable_cost, selling_price):
        query = f"SELECT * FROM break_even WHERE email = '{mail}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result) == 0:
            query = f"INSERT INTO break_even (email, fixed_cost, variable_cost, selling_price) VALUES ('{mail}', {fixed_cost}, {variable_cost}, {selling_price})"
            self.cursor.execute(query)
            self.mydb.commit()
            return "successfully created"
        else:
            query = f"UPDATE break_even SET fixed_cost = {fixed_cost}, variable_cost =  {variable_cost}, selling_price = {selling_price} WHERE email = '{mail}'"
            self.cursor.execute(query)
            self.mydb.commit()
            return "successfully updated"
        
    def get_break(self, mail):
        query = f"SELECT * FROM break_even WHERE email = '{mail}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            mail = row[0]
            fixed_cost = row[1]
            variable_cost = row[2]
            selling_price = row[3]
        
        contri_mpu = selling_price - variable_cost #contribution in margin per user
        breakeven = {}
        breakeven["be_users"] = fixed_cost/contri_mpu #breakeven point (in users)
        breakeven["be_revenue"] = breakeven["be_users"] * selling_price
        return [breakeven]
