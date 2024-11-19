from flask import Blueprint, jsonify, request
from db import db
import pyotp
import qrcode

users_collection = db["users"]

# Set up a blueprint for user signup
user_signup_bp = Blueprint('user_signup', _name_)

@user_signup_bp.route('/signup', methods=['POST'])
def signup():
    try:
        # Get user data from the request
        data = request.json
        email = data.get('email')

        # Validate input fields
        if not email:
            return jsonify({"error": "Email is required."}), 400

        # Check if email already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"error": "Email already exists."}), 400

        # Generate a TOTP secret key for the user
        secret = pyotp.random_base32()

        # Create user document
        user_data = {
            "email": email,
            "totp_secret": secret  # Store the TOTP secret in the database
        }

        # Insert the user document into the database
        users_collection.insert_one(user_data)

        # Generate a QR code for the user to scan in their authenticator app
        totp = pyotp.TOTP(secret)
        qr_code_data = totp.provisioning_uri(email, issuer_name="filterIt")
        qr_code_img = qrcode.make(qr_code_data)

        # Save QR code as a file (or send it to the front end as base64 for display)
        qr_code_img.save(f"{email}_qrcode.png")

        return jsonify({
            "message": "User registered successfully. Scan the QR code in your authenticator app.",
            "qr_code_data": qr_code_data  # Optional: Send the provisioning URI to the front end
        }), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500