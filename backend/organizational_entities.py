from flask import Blueprint, jsonify, request, current_app
from db import db
from bson import ObjectId
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
        label = data.get('label')
        terms = data.get('terms', [])

        if not label or not terms:
            return jsonify({"error": "Both label and terms are required"}), 400

        if entity_id:

            entity_object_id = ObjectId(entity_id)
            result = organizational_entities_collection.update_one(
                {"email": email, "organizational_entities._id": entity_object_id},
                {"$set": {"organizational_entities.$.label": label, "organizational_entities.$.terms": terms}}
            )
            if result.matched_count == 0:
                return jsonify({"error": "No matching entity found"}), 404
            message = f"Organizational entity '{label}' updated successfully."
        else:
            # Add new organizational entity
            new_entity = {
                "_id": ObjectId(),
                "label": "ORG",
                "terms": terms
            }
            organizational_entities_collection.update_one(
                {"email": email},
                {"$push": {"organizational_entities": new_entity}},
                upsert=True
            )
            message = f"Organizational entity '{label}' created successfully."

        return jsonify({"message": message}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@organizational_entities_bp.route('/get_organizational_entities', methods=['GET'])
def get_organizational_entities():
    try:
        # Get the email from the JWT token
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        email = decoded_token.get("user_email")
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        # Retrieve all organizational entities for the user
        user_entities = organizational_entities_collection.find_one(
            {"email": email},
            {"_id": 0, "organizational_entities": 1}
        )

        if not user_entities or "organizational_entities" not in user_entities:
            return jsonify({"organizational_entities": []}), 200  # Return an empty list if none found

        organizational_entities = [
            {
                "entity_id": str(entity["_id"]),
                "label": entity["label"],
                "terms": entity["terms"]
            }
            for entity in user_entities["organizational_entities"]
        ]

        return jsonify({"organizational_entities": organizational_entities}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
