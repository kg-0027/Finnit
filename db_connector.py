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
        for row in self.cursor.fetchall():
            student = {}
            student["enrollment"] = row[0]
            student["name"] = row[1]
            student["school"] = row[2]
            student["course"] = row[3]
            student["batch"] = row[4]
            student["hostel"] = row[5]
            student["mobile"] = row[6]
            student["email"] = row[7]
            return [student]
