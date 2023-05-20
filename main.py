from flask import Flask, jsonify, request
from db_connector import ItemDatabase
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


# Trial API
@app.route('/')
@cross_origin(origin='*')
def hello_world():
    return 'Hello, World!'


# get values from KPIs Table
@app.route('/kpi_table/getall', methods=["POST"])
@cross_origin(origin='*')
def get_medicine_details():
    data_json = request.get_json(force=True)


# create a post api to upload email, total_sale_and_marketing, total_revenu, "total_cust, user_stopped, cogs into the kpi_table"
@app.route('/kpi_table/create', methods=["POST"])
@cross_origin(origin='*')
def create_kpi():
    data_json = request.get_json(force=True)
    mail = data_json['email']
    total_sale_and_marketing = data_json['total_sale_and_marketing']
    total_revenue = data_json['total_revenue']
    total_cust = data_json['total_cust']
    user_stopped = data_json['user_stopped']
    cogs = data_json['cogs']
    result = db.create_kpi(mail, total_sale_and_marketing,
                           total_revenue, total_cust, user_stopped, cogs)
    return jsonify(result)


if __name__ == "__main__":
    global db
    db = ItemDatabase()
    app.run(debug=True)
