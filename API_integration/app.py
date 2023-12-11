from flask import Flask, jsonify,request 
from services import google_sheet_integration
import numpy as np

app = Flask(__name__)
doc_crus = google_sheet_integration.Document_CRUD()
doc_crus.Spreadsheet_ID = "1kpj7e08JrhsH4WKJhQeIYXWUh4k4Nc4vKSd-DuZqpVw"


def validate_schema1(data):
    required_keys = ['name', 'surname', 'age', 'email', 'phone']
    return all(key in data for key in required_keys)

@app.route("/")
def main():
    return "<h1>WELCOME TO GOOGLE SHEET API INEGRATION</h1>"



@app.route("/append", methods=['POST'])
def append():
    try:
        data = request.get_json()

        # Assuming the function is correctly named and imported
        if not validate_schema1(data):  
            return jsonify({"message": "Incorrect schema (POST /append | request_body = {name:str, age:int})"}), 400
        
        # process data (add data to google sheet)
        valueInputOption = "USER_ENTERED"
        range_name = "C8:G8"
        # values = [[str(data[dat]) for dat in data]]
        values = [[data[dat] if not dat == "phone" else str(f"\"{data['phone']}\"") for dat in data]]

        # Call append method
        append_result = doc_crus.append(range_name, valueInputOption, values)

        # Corrected string formatting
        return jsonify({"data":values, "append result":append_result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500