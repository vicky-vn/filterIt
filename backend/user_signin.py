from flask import Blueprint, jsonify, request, current_app
from db import db
import jwt
import datetime
import pyotp

users_collection = db["users"]

# Set up a blueprint for user signin
user_signin_bp = Blueprint('user_signin', _name_)

@user_signin_bp.route('/signin', methods=['POST'])
def signin():
    try:
        # Get email and token from the request
        data = request.json
        email = data.get('email')
        token = data.get('token')  # User's TOTP from their authenticator app

        # Validate input fields
        if not email or not token:
            return jsonify({"error": "Both email and token are required."}), 400

        # Retrieve the user document by email
        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"error": "Invalid email or token."}), 401

        # Verify the TOTP
        totp = pyotp.TOTP(user["totp_secret"])
        if not totp.verify(token):
            return jsonify({"error": "Invalid email or token."}), 401

        # Generate JWT token
        jwt_token = jwt.encode({
            "user_email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")

        return jsonify({"message": "Signin successful", "token": jwt_token}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500