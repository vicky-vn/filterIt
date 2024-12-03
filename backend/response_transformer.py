from db import db
from bson import ObjectId
import re
from flask import jsonify, Blueprint, request

response_bp = Blueprint('response', __name__)

def fetch_entity_mapping(document_id):
    try:
        document = db["uploads"].find_one({"_id": ObjectId(document_id)})
        if document:
            return document.get("entity_mapping", {})
        return {}
    except Exception as e:
        print(f"Error fetching entity mapping: {e}")
        return {}

def get_transformed_answer(gpt_response, document_id):
    entity_mapping = fetch_entity_mapping(document_id)

    if not entity_mapping:
        return gpt_response

    sorted_mapping = sorted(entity_mapping.items(), key=lambda x: len(x[0]), reverse=True)

    transformed_response = gpt_response
    for token, details in sorted_mapping:
        if isinstance(details, dict):
            actual_value = details.get("value")
            if actual_value:
                transformed_response = re.sub(re.escape(token), actual_value, transformed_response)

    return transformed_response

@response_bp.route("/transform_response", methods=["POST"])
def transform_response():
    try:
        data = request.json
        gpt_response = data.get("gpt_response")
        document_id = data.get("document_id")

        if not gpt_response or not document_id:
            return jsonify({"error": "'gpt_response' and 'document_id' are required"}), 400

        transformed_response = get_transformed_answer(gpt_response, document_id)

        return jsonify({
            "original_response": gpt_response,
            "transformed_response": transformed_response
        }), 200

    except Exception as e:
        print(f"Error transforming response: {e}")
        return jsonify({"error": str(e)}), 500
