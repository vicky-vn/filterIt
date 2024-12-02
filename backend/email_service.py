import sib_api_v3_sdk
from flask import Blueprint, jsonify, request
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import os

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = BREVO_API_KEY

email_bp = Blueprint("brevo_service", __name__)

@email_bp.route("/send_email", methods=["POST"])
def send_email():
    try:
        data = request.json
        sender_email = data.get("from", "awarenesspro@gmail.com")
        sender_name = data.get("sender_name", "Default Sender")
        recipients = data.get("to")
        subject = data.get("subject")
        html_content = data.get("html", "<strong>No content provided.</strong>")

        if not recipients or not subject:
            return jsonify({"error": "'to' and 'subject' are required"}), 400

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        email = sib_api_v3_sdk.SendSmtpEmail(
            sender={"email": sender_email, "name": sender_name},
            to=[{"email": recipient} for recipient in recipients],
            subject=subject,
            html_content=html_content,
        )

        response = api_instance.send_transac_email(email)
        return jsonify({"message": "Email sent successfully", "response": response.to_dict()}), 200

    except ApiException as e:
        print(f"Error sending email: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500
