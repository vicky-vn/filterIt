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
from pdf_generator import pdf_generator_bp
from question_transformer import get_transformed_question
from response_transformer import get_transformed_answer
from settings import settings_bp
from openai_integration import call_openai
from response_transformer import response_bp
from pdf_text_extractor import pdf_extractor_bp
from connected_apps import connected_apps_bp

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
app.register_blueprint(pdf_generator_bp)
app.register_blueprint(response_bp)
app.register_blueprint(pdf_extractor_bp)
app.register_blueprint(connected_apps_bp)



# Index route (welcome message)
@app.route('/', methods=['GET'])
def index():
    return "Welcome to filterIt!", 200

# Not in flow as of now
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


@app.route('/summarize', methods=['POST'])
def summarize():

    data = request.json
    #user_question = data.get("question")
    document_id = data.get("document_id")

    if not document_id:
        return jsonify({"error": "'document_id' is required"}), 400

    try:
        #transformed_question = get_transformed_question(user_question, document_id)

        document = collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            return jsonify({"error": "Document not found"}), 404

        tokenized_text = document.get("tokenized_text")
        #
        # messages = [
        #     {"role": "system", "content": f"You're experienced in summarizing health records and reports."},
        #     {"role": "user", "content": f"Use this information to summarize the report, make sure the summary is 1000 words. Have all the medical terms understandable to common folks. Format the content like a health report: {tokenized_text} + {transformed_question}"},
        # ]
        messages = [
            {"role": "system", "content": f"You're experienced in summarizing health records and reports."},
            {"role": "user",
             "content": f"Use the following information to summarize and make sure it is not more than 2000 words. Have all the medical terms understandable to common folks. Format the content like a health report and give me the summary alone, do not add any formating: {tokenized_text}"},
        ]

        gpt_response = call_openai(messages)
        print(gpt_response)
        if not gpt_response:
            return jsonify({"error": "Failed to get a response from OpenAI."}), 500

        demasked_response = get_transformed_answer(gpt_response, document_id)

        collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {
                "gpt_response": gpt_response,
                "demasked_response": demasked_response
            }}
        )

        return jsonify({
            "gpt_response": gpt_response,
            "demasked_response": demasked_response
        }), 200


    except Exception as e:
        print(f"Error in ask_question route: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)