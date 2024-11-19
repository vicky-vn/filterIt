from flask import Blueprint, jsonify, request
from db import db
settings_bp = Blueprint('settings', _name_)

# Define MongoDB collections for settings
settings_collection = db["settings"]

# POST API to save the choice of LLM
@settings_bp.route('/save_llm_choice', methods=['POST'])
def save_llm_choice():
    try:
        data = request.json
        llm_choice = data.get('llm_choice', None)

        if not llm_choice:
            return jsonify({"error": "LLM choice is required."}), 400

        settings_collection.update_one({}, {"$set": {"llm_choice": llm_choice}}, upsert=True)

        return jsonify({"message": "LLM choice saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET API to save the choice of LLM
@settings_bp.route('/get_llm_choice', methods=['GET'])
def get_llm_choice():
    try:
        # Retrieve the LLM choice
        settings = settings_collection.find_one({}, {"_id": 0, "llm_choice": 1})

        if not settings or "llm_choice" not in settings:
            return jsonify({"llm_choice": None, "message": "No LLM choice set."}), 200

        return jsonify({"llm_choice": settings["llm_choice"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500