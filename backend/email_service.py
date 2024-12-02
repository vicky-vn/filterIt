import os
import resend
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
email_bp = Blueprint("email_service", __name__)

@email_bp.route("/send_email", methods=["POST"])
def send_email():
    try:
        data = request.json
        sender = data.get("from", "onboarding@resend.dev")
        recipients = data.get("to")
        subject = data.get("subject")
        html_content = data.get("html", "<strong>No content provided.</strong>")

        if not recipients or not subject:
            return jsonify({"error": "'to' and 'subject' are required"}), 400

        params = {
            "from": sender,
            "to": recipients,
            "subject": subject,
            "html": html_content,
        }

        response = resend.Emails.send(params)
        return jsonify({"message": "Email sent successfully", "response": response}), 200

    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({"error": str(e)}), 500