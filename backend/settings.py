from flask import Blueprint, jsonify, request
from db import db  # Assuming you have your MongoDB setup here

# Set up a blueprint for settings
settings_bp = Blueprint('settings', __name__)

# Define MongoDB collections for settings
settings_collection = db["settings"]  # Create a collection to store settings

# POST API to save organizational information keywords
@settings_bp.route('/save_organizational_info', methods=['POST'])
def save_organizational_info():
    try:
        data = request.json
        keywords = data.get('keywords', '')  # Expecting a comma-separated string
        keywords_list = [keyword.strip() for keyword in keywords.split(',')]  # Split and clean

        # Save to MongoDB
        settings_collection.update_one({}, {"$set": {"organizational_info": keywords_list}}, upsert=True)

        return jsonify({"message": "Organizational information saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST API to save custom information keywords
@settings_bp.route('/save_custom_info', methods=['POST'])
def save_custom_info():
    try:
        data = request.json
        keywords = data.get('keywords', '')  # Expecting a comma-separated string
        keywords_list = [keyword.strip() for keyword in keywords.split(',')]  # Split and clean

        # Save to MongoDB
        settings_collection.update_one({}, {"$set": {"custom_info": keywords_list}}, upsert=True)

        return jsonify({"message": "Custom information saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST API to save the choice of LLM
@settings_bp.route('/save_llm_choice', methods=['POST'])
def save_llm_choice():
    try:
        data = request.json
        llm_choice = data.get('llm_choice', None)

        if not llm_choice:
            return jsonify({"error": "LLM choice is required."}), 400

        # Save to MongoDB
        settings_collection.update_one({}, {"$set": {"llm_choice": llm_choice}}, upsert=True)

        return jsonify({"message": "LLM choice saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
