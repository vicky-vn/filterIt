from flask import Flask, jsonify, request
from db import collection  

app = Flask(__name__)

# Index route
@app.route('/', methods=['GET'])
def index():
    return "Welcome to MedRecShield Application!!"

# GET API to retrieve all records from the patient_records collection
@app.route('/get_patient_records', methods=['GET'])
def get_patient_records():
    try:
        records = list(collection.find())  # Fetch documents from MongoDB
        output = []
        for record in records:
            record['_id'] = str(record['_id'])  # Convert ObjectId to string
            output.append(record)
        return jsonify(output), 200
    except Exception as e:
        print(f"Error: {e}")  # Print any error messages to the console
        return jsonify({"error": str(e)}), 500

# POST API to add a new record to the patient_records collection
@app.route('/add_patient_record', methods=['POST'])
def add_patient_record():
    try:
        data = request.get_json()
        result = collection.insert_one(data)
        return jsonify({"inserted_id": str(result.inserted_id)}), 201
    except Exception as e:
        print(f"Error: {e}")  # Print any error messages to the console
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=3000)

