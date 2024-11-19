from db import db
from bson import ObjectId
import re

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
    for token, actual_value in sorted_mapping:
        transformed_response = re.sub(re.escape(token), actual_value, transformed_response)

    return transformed_response