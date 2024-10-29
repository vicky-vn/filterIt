from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt
import re
from db import db  # Import the `db` instance from db.py

# Initialize Flask bcrypt for password hashing
bcrypt = Bcrypt()

# Define the collection for users
users_collection = db["users"]

# Set up a blueprint for user signup
user_signup_bp = Blueprint('user_signup', __name__)

# Email regex pattern for validation
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def generate_user_id():
    # Count existing users to create the next user ID
    user_count = users_collection.count_documents({})
    # Format user ID as user001, user002, etc.
    return f"user{user_count + 1:03}"

@user_signup_bp.route('/signup', methods=['POST'])
def signup():
    try:
        # Get user data from the request
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validate input fields
        if not username or not email or not password:
            return jsonify({"error": "All fields (username, email, password) are required."}), 400

        if not EMAIL_REGEX.match(email):
            return jsonify({"error": "Invalid email format."}), 400

        # Check if username or email already exists
        if users_collection.find_one({"username": username}):
            return jsonify({"error": "Username already exists."}), 400
        if users_collection.find_one({"email": email}):
            return jsonify({"error": "Email already exists."}), 400

        # Generate a simple user ID
        user_id = generate_user_id()

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create user document
        user_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "password": hashed_password
        }

        # Insert the user document into the database
        users_collection.insert_one(user_data)

        return jsonify({"message": "User registered successfully.", "user_id": user_id}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500