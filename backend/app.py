import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from db import collection
from bson import ObjectId

from user_signup import user_signup_bp
from user_signin import user_signin_bp
from input_processor import input_processor_bp
from custom_entities import custom_entities_bp
from organizational_entities import organizational_entities_bp
from parameterized_pdf_generator import parameterized_pdf_generator_bp
from question_transformer import get_transformed_question
from response_transformer import get_transformed_answer
from settings import settings_bp

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# JWT Secret Key from environment
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
if not app.config['JWT_SECRET_KEY']:
    raise ValueError("JWT_SECRET_KEY environment variable is not set!")

# Register blueprints
app.register_blueprint(user_signup_bp)
app.register_blueprint(user_signin_bp)
app.register_blueprint(input_processor_bp)
app.register_blueprint(custom_entities_bp)
app.register_blueprint(organizational_entities_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(parameterized_pdf_generator_bp)


# Index route (welcome message)
@app.route('/', methods=['GET'])
def index():
    return "Welcome to filterIt!", 200

@app.route('/transform_question', methods=['POST'])
def transform_question_route():

    data = request.json
    user_question = data.get("question")
    document_id = data.get("document_id")

    if not user_question or not document_id:
        return jsonify({"error": "Both 'question' and 'document_id' are required"}), 400

    try:
        transformed_question = get_transformed_question(user_question, document_id)
        return jsonify({"transformed_question": transformed_question}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/transform_answer', methods=['POST'])
def transform_answer_route():

    data = request.json
    gpt_response = data.get("gpt_response")
    document_id = data.get("document_id")

    if not gpt_response or not document_id:
        return jsonify({"error": "Both 'gpt_response' and 'document_id' are required"}), 400

    try:
        transformed_response = get_transformed_answer(gpt_response, document_id)
        return jsonify({"demasked_response": transformed_response}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ask_question', methods=['POST'])
def ask_question():

    data = request.json
    user_question = data.get("question")
    document_id = data.get("document_id")

    if not user_question or not document_id:
        return jsonify({"error": "Both 'question' and 'document_id' are required"}), 400

    try:
        transformed_question = get_transformed_question(user_question, document_id)

        document = collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            return jsonify({"error": "Document not found"}), 404

        tokenized_text = document.get("tokenized_text")

        simulated_gpt_response = "[PERSON_1] is GOAT"

        transformed_response = get_transformed_answer(simulated_gpt_response, document_id)

        return jsonify({
            "gpt_response": simulated_gpt_response,
            "demasked_response": transformed_response
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)