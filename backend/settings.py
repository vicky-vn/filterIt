from flask import Blueprint, jsonify, request, current_app
import jwt
from db import db
settings_bp = Blueprint('settings', __name__)

settings_collection = db["settings"]

ALLOWED_LLM_CHOICES = ["OpenAI", "Claude"]


@settings_bp.route('/save_llm_choice', methods=['PUT'])
def save_llm_choice():
    try:
        token = request.headers.get('Authorization', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        user_email = decoded_token.get("user_email")
        if not user_email:
            return jsonify({"error": "User email is missing in token!"}), 400

        data = request.json
        llm_choice = data.get('llm_choice', None)
        if not llm_choice:
            return jsonify({"error": "LLM choice is required."}), 400

        if llm_choice not in ALLOWED_LLM_CHOICES:
            return jsonify({"error": f"Invalid LLM choice. Allowed choices are: {', '.join(ALLOWED_LLM_CHOICES)}"}), 400

        settings_collection.update_one(
            {"email": user_email},
            {"$set": {"llm_choice": llm_choice}},
            upsert=True
        )

        return jsonify({"message": "LLM choice updated successfully."}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@settings_bp.route('/get_llm_choice', methods=['GET'])
def get_llm_choice():
    try:
        token = request.headers.get('Authorization', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        user_email = decoded_token.get("user_email")
        if not user_email:
            return jsonify({"error": "User email is missing in token!"}), 400

        settings = settings_collection.find_one({"email": user_email}, {"_id": 0, "llm_choice": 1})

        if not settings or "llm_choice" not in settings:
            return jsonify({"llm_choice": None, "message": "No LLM choice set."}), 200

        return jsonify({"llm_choice": settings["llm_choice"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
