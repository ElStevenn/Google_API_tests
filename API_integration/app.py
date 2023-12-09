from flask import Flask, jsonify,request 


app = Flask(__name__)

def validate_schema1(data):
    required_keys = ['name', 'surname', 'age', 'email']
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


        # Corrected string formatting
        return jsonify({"message": f"The datahas been proecesed in the google sheet"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500