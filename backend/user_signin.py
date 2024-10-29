from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash
from flask_bcrypt import Bcrypt
from db import db  # Import the `db` instance from db.py
import jwt
import datetime

# Initialize bcrypt for password verification
bcrypt = Bcrypt()

# Define the collection for users
users_collection = db["users"]

# Set up a blueprint for user signin
user_signin_bp = Blueprint('user_signin', __name__)

@user_signin_bp.route('/signin', methods=['POST'])
def signin():
    try:
        # Get username and password from the request
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Validate input fields
        if not username or not password:
            return jsonify({"error": "Both username and password are required."}), 400

        # Retrieve the user document by username
        user = users_collection.find_one({"username": username})

        if not user:
            return jsonify({"error": "Invalid username or password."}), 401

        # Verify the password
        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid username or password."}), 401

        # Generate JWT token
        token = jwt.encode({
            "user_id": user["user_id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")

        # If successful, return a success message with the token
        return jsonify({"message": "Signin successful", "token": token}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
