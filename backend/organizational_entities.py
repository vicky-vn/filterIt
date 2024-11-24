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

        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        email = decoded_token.get("user_email")  # Extract email
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        data = request.json
        entity_id = data.get('entity_id')
        terms = data.get('terms', [])  # Default to an empty list if no terms are provided

        # Normalize terms to lowercase
        terms = [term.strip().lower() for term in terms]

        if entity_id:
            # Update existing organizational entity
            entity_object_id = ObjectId(entity_id)
            result = organizational_entities_collection.update_one(
                {"email": email, "organizational_entities._id": entity_object_id},
                {"$set": {"organizational_entities.$.terms": terms}}
            )
            if result.matched_count == 0:
                return jsonify({"error": "No matching entity found"}), 404
            message = f"Organizational entity updated successfully."
        else:
            # Add new organizational entity
            new_entity = {
                "_id": ObjectId(),
                "label": "ORG",  # Default label for organizational entity
                "terms": terms
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

        user_entity = organizational_entities_collection.find_one(
            {"email": email},
            {"_id": 0, "organizational_entity": 1}
        )

        if not user_entity or "organizational_entity" not in user_entity:
            return jsonify({"organizational_entity": None}), 200

        return jsonify({"organizational_entity": user_entity["organizational_entity"]}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
