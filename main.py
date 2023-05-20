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
    mail = data_json['email']
    details = db.get_kpi(mail)
    return jsonify(details)


if __name__ == "__main__":
    global db
    db = ItemDatabase()
    app.run(debug=True)