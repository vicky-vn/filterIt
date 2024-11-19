import re
from db import db
from bson import ObjectId

def fetch_entity_mapping(document_id):
    document = db["uploads"].find_one({"_id": ObjectId(document_id)})
    if document:
        return document.get("entity_mapping", {})
    return {}

def transform_question(user_question, entity_mapping):
    transformed_question = user_question
    sorted_entities = sorted(entity_mapping.items(), key=lambda x: len(x[1]), reverse=True)

    for token, entity_name in sorted_entities:
        transformed_question = re.sub(re.escape(entity_name), token, transformed_question, flags=re.IGNORECASE)

    return transformed_question

def get_transformed_question(user_question, document_id):
    entity_mapping = fetch_entity_mapping(document_id)
    return transform_question(user_question, entity_mapping)