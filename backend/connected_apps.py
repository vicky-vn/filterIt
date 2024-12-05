from flask import Blueprint, request, jsonify, current_app
from db import db
from bson import ObjectId
import jwt

connected_apps_bp = Blueprint("connected_apps", __name__)
connected_apps_collection = db["connected_apps"]

@connected_apps_bp.route("/create_app", methods=["POST"])
def create_app():
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        email = decoded_token.get("user_email")
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        data = request.json
        name = data.get("name")
        description = data.get("description")
        watch_endpoint = data.get("watch_endpoint")
        interceptor_code = data.get("interceptor_code")

        if not all([name, description, watch_endpoint, interceptor_code]):
            return jsonify({"error": "All fields are required"}), 400

        new_app = {
            "email": email,
            "name": name,
            "description": description,
            "watch_endpoint": watch_endpoint,
            "interceptor_code": interceptor_code,
        }

        result = connected_apps_collection.insert_one(new_app)
        return jsonify({"message": "App created successfully", "app_id": str(result.inserted_id)}), 201

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error creating app: {e}")
        return jsonify({"error": str(e)}), 500

@connected_apps_bp.route("/delete_app/<app_id>", methods=["DELETE"])
def delete_app(app_id):
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        email = decoded_token.get("user_email")
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        # Delete the app only if it belongs to the user
        result = connected_apps_collection.delete_one({"_id": ObjectId(app_id), "email": email})
        if result.deleted_count == 0:
            return jsonify({"error": "App not found or does not belong to the user"}), 404

        return jsonify({"message": "App deleted successfully"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error deleting app: {e}")
        return jsonify({"error": str(e)}), 500

@connected_apps_bp.route("/get_apps", methods=["GET"])
def get_apps():
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        email = decoded_token.get("user_email")
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        # Fetch all apps belonging to the user
        apps = list(connected_apps_collection.find({"email": email}))
        for app in apps:
            app["_id"] = str(app["_id"])  # Convert ObjectId to string for JSON response

        return jsonify({"apps": apps}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error fetching apps: {e}")
        return jsonify({"error": str(e)}), 500

@connected_apps_bp.route("/update_app/<app_id>", methods=["PUT"])
def update_app(app_id):
    try:
        # Decode JWT token to get email
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        email = decoded_token.get("user_email")
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        data = request.json
        valid_fields = {key: value for key, value in data.items() if key in ["name", "description", "watch_endpoint", "interceptor_code"]}

        if not valid_fields:
            return jsonify({"error": "No valid fields provided for update"}), 400

        # Update the app only if it belongs to the user
        result = connected_apps_collection.update_one(
            {"_id": ObjectId(app_id), "email": email},
            {"$set": valid_fields}
        )

        if result.matched_count == 0:
            return jsonify({"error": "App not found or does not belong to the user"}), 404

        return jsonify({"message": "App updated successfully"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error updating app: {e}")
        return jsonify({"error": str(e)}), 500
