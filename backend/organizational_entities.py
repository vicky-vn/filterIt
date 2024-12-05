from bson import ObjectId
from flask import Blueprint, jsonify, request, current_app
from db import db
import jwt

organizational_entities_bp = Blueprint('organizational_entities', __name__)

organizational_entities_collection = db["organizational_entities"]


@organizational_entities_bp.route('/update_organizational_entity', methods=['PUT'])
def update_organizational_entity():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        # Decode the JWT token to get the email
        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        email = decoded_token.get("user_email")  # Extract email
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        data = request.json
        entity_id = data.get('entity_id')  # Optional
        terms = data.get('terms', [])  # list of terms from the frontend

        if not isinstance(terms, list):
            return jsonify({"error": "Terms must be a list"}), 400

        # Normalize terms
        normalized_terms = []
        for term in terms:
            if isinstance(term, str):  # Ensure term is a string
                normalized_terms.extend([t.strip() for t in term.split(",")])  # Split by commas and strip whitespace

        # Remove duplicates and empty values
        normalized_terms = list(set(filter(None, normalized_terms)))

        if not normalized_terms:
            return jsonify({"error": "No valid terms provided"}), 400

        if entity_id:
            # Update an existing organizational entity
            entity_object_id = ObjectId(entity_id)

            # Update the terms array for the specific entity
            result = organizational_entities_collection.update_one(
                {"email": email, "organizational_entities._id": entity_object_id},
                {"$set": {"organizational_entities.$.terms": normalized_terms}}
            )

            if result.matched_count == 0:
                return jsonify({"error": "No matching entity found"}), 404
            message = "Organizational entity updated successfully."
        else:
            # Check if any organizational entities already exist for the user
            existing_entity = organizational_entities_collection.find_one({"email": email})

            if existing_entity:
                # Update the terms array in the first organizational entity
                organizational_entities_collection.update_one(
                    {"email": email},
                    {"$set": {"organizational_entities.0.terms": normalized_terms}}
                )
                message = "Organizational entity updated successfully."
            else:
                # Create a new organizational entity
                new_entity = {
                    "_id": ObjectId(),
                    "label": "ORG",  # Default label for organizational entity
                    "terms": normalized_terms
                }
                organizational_entities_collection.update_one(
                    {"email": email},
                    {"$push": {"organizational_entities": new_entity}},
                    upsert=True
                )
                message = "Organizational entity created successfully."

        return jsonify({"message": message}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@organizational_entities_bp.route('/get_organizational_entity', methods=['GET'])
def get_organizational_entity():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        email = decoded_token.get("user_email")
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        # Fetch organizational entities for the user
        user_entity = organizational_entities_collection.find_one(
            {"email": email},
            {"_id": 0, "organizational_entities": 1}
        )

        # If no organizational entities exist, return null
        if not user_entity or "organizational_entities" not in user_entity:
            return jsonify({"organizational_entity": {"terms": []}}), 200

        # Flatten the terms into a single list
        terms = [term for entity in user_entity["organizational_entities"] for term in entity["terms"]]

        # Return response with `organizational_entity` key
        return jsonify({"organizational_entity": {"terms": terms}}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
