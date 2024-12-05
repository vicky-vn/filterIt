from flask import Blueprint, jsonify, request
from db import db
import pyotp
import qrcode
import io
import base64

users_collection = db["users"]
user_signup_bp = Blueprint('user_signup', __name__)

@user_signup_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')

        if not email:
            return jsonify({"error": "Email is required."}), 400

        # Check if email already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"error": "Email already exists."}), 400

        # Generate a TOTP secret key for the user
        secret = pyotp.random_base32()

        user_data = {
            "email": email,
            "totp_secret": secret
        }

        users_collection.insert_one(user_data)

        # Generate a QR code for the user to scan in their authenticator app
        totp = pyotp.TOTP(secret)
        qr_code_data = totp.provisioning_uri(email, issuer_name="filterIt")
        qr_code_img = qrcode.make(qr_code_data)

        # Convert the QR code image to a Base64-encoded string
        buffered = io.BytesIO()
        qr_code_img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({
            "message": "User registered successfully. Scan the QR code in your authenticator app.",
            "qr_code_base64": "data:image/png;base64,"+ qr_code_base64  # Base64-encoded QR code image
        }), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
