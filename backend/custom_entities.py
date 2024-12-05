from flask import Blueprint, jsonify, request, current_app
from db import db
from bson import ObjectId
import jwt
custom_entities_bp = Blueprint('custom_entities', __name__)

custom_entities_collection = db["custom_entities"]

@custom_entities_bp.route('/update_custom_entity', methods=['PUT'])
def update_custom_entity():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        email = decoded_token.get("user_email")  # Extract email
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        # Retrieve entity_id (optional), label, and terms from the request JSON
        data = request.json
        entity_id = data.get('entity_id')  # Optional for renaming
        label = data.get('label')
        terms = data.get('terms', [])

        if not label or not terms:
            return jsonify({"error": "Both label and terms are required"}), 400

        # Normalize terms to lowercase and deduplicate
        terms = list(set([term.strip().lower() for term in terms]))

        if entity_id:
            # Update the existing custom entity by entity_id
            entity_object_id = ObjectId(entity_id)
            result = custom_entities_collection.update_one(
                {"email": email, "custom_entities._id": entity_object_id},
                {"$set": {
                    "custom_entities.$.label": label,
                    "custom_entities.$.terms": terms
                }}
            )
            if result.matched_count == 0:
                return jsonify({"error": "No matching entity found"}), 404
            message = f"Custom entity with ID '{entity_id}' updated successfully."
        else:
            # Check if a custom entity with the same label already exists
            existing_entity = custom_entities_collection.find_one(
                {"email": email, "custom_entities.label": label}
            )

            if existing_entity:
                # Merge and deduplicate terms if the label already exists
                custom_entities_collection.update_one(
                    {"email": email, "custom_entities.label": label},
                    {"$set": {"custom_entities.$.terms": terms}}
                )
                message = f"Custom entity '{label}' updated successfully."
            else:
                # Add a new custom entity if no existing label is found
                new_entity = {
                    "_id": ObjectId(),
                    "label": label,
                    "terms": terms
                }
                custom_entities_collection.update_one(
                    {"email": email},
                    {"$push": {"custom_entities": new_entity}},
                    upsert=True
                )
                message = f"Custom entity '{label}' created successfully."

        return jsonify({"message": message}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@custom_entities_bp.route('/get_custom_entities', methods=['GET'])
def get_custom_entities():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        email = decoded_token.get("user_email")  # Extract email
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        # Retrieve all custom entities for the user
        user_entities = custom_entities_collection.find_one(
            {"email": email},
            {"_id": 0, "custom_entities": 1}
        )

        if not user_entities or "custom_entities" not in user_entities:
            return jsonify({"custom_entities": []}), 200  # Return an empty list if none found

        # Format response to include ObjectId as a string
        custom_entities = [
            {
                "entity_id": str(entity["_id"]),
                "label": entity["label"],
                "terms": entity["terms"]
            }
            for entity in user_entities["custom_entities"]
        ]

        return jsonify({"custom_entities": custom_entities}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500